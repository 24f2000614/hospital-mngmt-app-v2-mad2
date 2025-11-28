<script setup>
import { get } from '../utils'
import { getToken } from '@/auth'
import { onMounted, reactive, ref, watch, computed, onBeforeMount } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const depts = ref([])
const initialData = ref(null)
const doctors = ref([])
const dates = ref([])
const error = ref('')
const token = getToken()
const route = useRoute()
const router = useRouter()
const id = route.params.id
const emit = defineEmits(['refresh'])
const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

const props = defineProps({
  isProgressive: Boolean,
})

const form = reactive({
  dept_id: null,
  d_id: null,
  date: null,
  start_time: null,
  status: 'Booked'
})


const showDoctor = computed(() => props.isProgressive ? form.dept_id : true)
const showDate   = computed(() => props.isProgressive ? form.d_id : true)
const showSlot   = computed(() => props.isProgressive ? form.date : true)
const showSubmit = computed(() => props.isProgressive ? form.start_time : true)

const bookAppointment =  async() =>{
  const method = props.isProgressive ? 'POST' : 'PUT'
  const base = 'http://127.0.0.1:5000/patient/appointments'
  const url = props.isProgressive ? base : base + `/${id}` 
  try{
    const req = await fetch(url, {
      method: method,
      headers: {
        'Content-Type' : 'application/json',
        'Authorization' : `Bearer ${token}`
      },
      body: JSON.stringify(form)
    })
    if (req.ok){
      alert("Booked Successfully")
      emit('refresh')
    }
    for (const key in form) {
      form[key] = ''; 
    }
  } catch (e) {
    error.value = e.message
    console.log(e.message)
  }
}

const cancelAppointment = async() => {
    const url = `http://127.0.0.1:5000/patient/appointments/${route.params.id}`
    await fetch(url, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    })
    router.push({ path: "/" + route.fullPath.split('/').slice(1, -1).join('/')})
    emit('refresh')
}

if (props.isProgressive){
  onMounted(async () => {
    try {
      depts.value = await get('http://127.0.0.1:5000/patient/dept')
    }catch (e) {
      error.value = e.message
    }
  })

  watch(() => form.dept_id, async id => {
    if (!id) return
    form.d_id = null
    const res = await get(`http://127.0.0.1:5000/patient/dept/${id}`)
    doctors.value = res['doctor_list']
  })

  watch(() => form.d_id, async id => {
    if (!id) return
      form.date = null
      dates.value = await get(`http://127.0.0.1:5000/patient/doc-availability/${id}`)
    console.log(dates.value)
  })

}else {
    onMounted(async () => {
    try {
      watch(() => route.params.id, async () => {
        initialData.value = await get(`http://127.0.0.1:5000/patient/appointments/${id}`);
        console.log(initialData)
        Object.assign(form, initialData);
      }, )
      initialData.value = await get(`http://127.0.0.1:5000/patient/appointments/${id}`)
      const d_id = initialData.value.appointment.d_id
      const doc = await get(`http://127.0.0.1:5000/patient/doctor-info/${d_id}`)
      const dept = await get(`http://127.0.0.1:5000/patient/dept/${doc.dept_id}`)
      doctors.value = [doc.name, dept.dept.name, doc.email]
      dates.value = await get(`http://127.0.0.1:5000/patient/doc-availability/${doc.d_id}`)
      console.log(doctors.value)
      Object.assign(form, initialData.value.appointment)
      const dateObj = new Date(form.start_time)
      form.date = `${days[dateObj.getUTCDay()]} ${String(dateObj.getUTCDate()).padStart(2, '0')}-${dateObj.getMonth() + 1}-${dateObj.getFullYear()}`;
      form.start_time = dateObj.getUTCHours()
      form.dept_id = doc.dept_id
      console.log(form.date)
      console.log(dates)
    }catch (e) {
      error.value = e.message
    }
  })
}

</script>

<template>
    <h2>Book Appointment</h2>
    <form @submit.prevent="bookAppointment">
      <div class="mb-3" v-if="isProgressive">
        <label class="form-label fw-bold">Department</label>
        <select v-model="form.dept_id" name="department" id="department" class="form-select" :disabled="!isProgressive">
          <option :value="dept.dept_id" v-for="dept in depts">{{ dept.name }}</option>
        </select>
      </div>
      <div class="mb-3" v-if="!isProgressive">
        <label class="form-label fw-bold">Department</label>
        <li class="list-group-item">{{ doctors[1] }}</li>
      </div>

      <div class="mb-3" v-if="showDoctor && isProgressive">
        <label class="form-label fw-bold">Doctor</label>
        <select name="doctor" id="doctor" class="form-select" v-model="form.d_id" :disabled="!isProgressive">
          <option :value="doc.d_id" v-for="doc in doctors">{{ doc.name }}</option>
        </select>
      </div>
      
      <div class="mb-3" v-if="!isProgressive">
        <label class="form-label fw-bold">Doctor</label>
        <li class="list-group-item"> {{ doctors[0] }}</li>
      </div>

      <div class="mb-3" v-if="!isProgressive">
        <label class="form-label fw-bold">Contact</label>
        <li class="list-group-item"> {{ doctors[2] }}</li>
      </div>

      <div class="mb-3" v-if="showDate && isProgressive">
        <label class="form-label fw-bold">Date</label>
        <select name="days" id="days" class="form-select" v-model="form.date" :disabled="!isProgressive">
          <option :value="day.date" v-for="day in dates" :disabled="!day['available']">{{ day.date }}</option>
        </select>
      </div>
      
      <div class="mb-3" v-if="showSlot">
        <label class="form-label fw-bold">Time Slot</label>
        <select name="slot" id="slot" class="form-select" v-model="form.start_time">
          <option v-if="!form.date" disabled value="">Select a date first</option>
          <option :value="slot[0]" :key="slot[0]" v-for="slot in dates.find(obj => obj.date === form.date)?.slots" :disabled="!slot[1]">{{ slot[0] }}:00</option>
        </select>
      </div>

      <div class="mb-3" v-if="showSubmit">
        <input type="submit" :value="isProgressive ? 'Book': 'Reschedule'" class="btn btn-primary form-control">
      </div>
    </form>
      <div class="mb-3" v-if="!isProgressive">
        <button class="btn btn-danger form-control my-1" @click="cancelAppointment">Cancel</button>
      </div>
    <div v-if="error" class="text-danger">{{ error }}</div>

</template>

