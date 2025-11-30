<script setup>
import { get } from '../utils'
import { getToken } from '@/auth'
import { onMounted, reactive, ref, watch, computed } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

const depts = ref([])
const initialData = ref(null)
const userItems = ref({})
const dates = ref([])
const newMed = ref('')
const error = ref('')
const token = getToken()
const route = useRoute()
const router = useRouter()
const id = route.params.id
const emit = defineEmits(['refresh'])
const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const prescriptions = ref([])

const props = defineProps({
  heading: String,
  isProgressive: Boolean,
  View: String,
  isHistorical: Boolean,
  user: String
})

const form = reactive({
  dept_id: null,
  p_id: null,
  d_id: null,
  date: null,
  start_time: null,
  status: 'Booked',
  diagnosis: null,
  prescriptions: []
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
      router.push({ path: "/" + route.fullPath.split('/').slice(1, -1).join('/')})
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
    const url = `http://127.0.0.1:5000/${props.View}/appointments/${route.params.id}`
    try{
      const result = await fetch(url, {
          method: 'DELETE',
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          }
      })
      
      router.push({ path: "/" + route.fullPath.split('/').slice(1, -1).join('/')})
      emit('refresh')
    }catch(e) {
      console.log(e.message)
      error.value = e.message
    }
}

const diagnose = async() => {
  try {
    const req = await fetch(`http://127.0.0.1:5000/doctor/appointments/${route.params.id}`, {
      method: 'POST',
      headers: {
        "Content-Type" : "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(form)
    })
    if (req.ok){
      alert("Updated Diagnosis")
    }
  } catch(e){
    console.log(e)
    error.value = e.message
  }
}

const markComplete = async() =>{
  try {
    const req = await fetch(`http://127.0.0.1:5000/doctor/appointments/${route.params.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': "application/json",
        'Authorization': `Bearer ${token}`
      }
    })
    if (req.ok){
      alert("Marked as Complete")
      emit('refresh')
    }
  } catch (e) {
    console.log(e)
    error.value = e.message
  }
}

const addMed = async () => {
  if (!newMed.value) return
  try {
      const req = await fetch(`http://127.0.0.1:5000/doctor/prescription`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({"a_id": id, "medicine": newMed.value})
      })
      const res = await req.json()
      prescriptions.value.push(res)
      newMed.value = ''
    } catch (e) {
      console.log(e)
      error.value = e.message
      return 
    }
}

const remMed = async(pr_id) => {
  const item = prescriptions.value.find(p => p.pr_id === pr_id)

  if (!item) return 

  if (form.prescriptions.some(p => p.pr_id === item.pr_id)) {
    try {
      await fetch(`http://127.0.0.1:5000/doctor/prescription/${item.pr_id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      })
    } catch (e) {
      console.log(e)
      error.value = e.message
      return 
    }
  }

  prescriptions.value = prescriptions.value.filter(p => p.pr_id !== pr_id)
  form.prescriptions = form.prescriptions.filter(p => p.pr_id !== pr_id)
}

if (props.isProgressive){
  onMounted(async () => {
    try {
      depts.value = await get('http://127.0.0.1:5000/patient/dept')
    }catch (e) {
      error.value = e.message
      console.log(e)
    }
  })

  watch(() => form.dept_id, async id => {
    if (!id) return
    form.d_id = null
    const res = await get(`http://127.0.0.1:5000/patient/dept/${id}`)
    userItems.value = res['doctor_list']
  })

  watch(() => form.d_id, async id => {
    if (!id) return
      form.date = null
      dates.value = await get(`http://127.0.0.1:5000/patient/doc-availability/${id}`)
  })

}else {
    onMounted(async () => {
    try {
      watch(() => route.params.id, async () => {
        initialData.value = await get(`http://127.0.0.1:5000/${props.View}/appointments/${id}`);
        Object.assign(form, initialData);
      }, )
      initialData.value = await get(`http://127.0.0.1:5000/${props.View}/appointments/${id}`)
      prescriptions.value = initialData.value.prescriptions || []
      if (props.View == 'patient'){
        const d_id = initialData.value.appointment.d_id
        const doc = await get(`http://127.0.0.1:5000/patient/doctor-info/${d_id}`)
        const dept = await get(`http://127.0.0.1:5000/patient/dept/${doc.dept_id}`)
        userItems.value = {"name": doc.name, "dept": dept.dept.name, "email":doc.email}
        dates.value = await get(`http://127.0.0.1:5000/patient/doc-availability/${doc.d_id}`)
        Object.assign(form, initialData.value.appointment)
        const dateObj = new Date(form.start_time)
        form.date = `${days[dateObj.getUTCDay()]} ${String(dateObj.getUTCDate()).padStart(2, '0')}-${dateObj.getMonth() + 1}-${dateObj.getFullYear()}`;
        form.start_time = dateObj.getUTCHours()
        form.dept_id = doc.dept_id
      } else if (props.View == 'doctor') {
        const p_id = initialData.value.appointment.p_id
        const patient = await get(`http://127.0.0.1:5000/doctor/patient-info/${p_id}`)
        userItems.value = {"name":patient.name, "email": patient.email, "phone_no": patient.phone_no}
        Object.assign(form, initialData.value.appointment)
        form.prescriptions = initialData.value.prescriptions
        const dateObj = new Date(form.start_time)
        form.start_time = dateObj.getUTCHours()
        form.date = `${days[dateObj.getDay()]} ${dateObj.getUTCDate()}-${dateObj.getMonth()+1}-${dateObj.getFullYear()}`
      }
    }catch (e) {
      console.log(e)
      error.value = e.message
    }
  })
}

</script>

<template>
    <h2>{{ props.heading }}</h2>
    <form @submit.prevent="bookAppointment">
      <div class="mb-3" v-if="isProgressive">
        <label class="form-label fw-bold">Department</label>
        <select v-model="form.dept_id" name="department" id="department" class="form-select" :disabled="!isProgressive">
          <option :value="dept.dept_id" v-for="dept in depts">{{ dept.name }}</option>
        </select>
      </div>
      <div class="mb-3" v-if="!isProgressive && View =='patient'">
        <label class="form-label fw-bold">Department</label>
        <li class="list-group-item">{{ userItems.dept }}</li>
      </div>

      <div class="mb-3" v-if="showDoctor && isProgressive">
        <label class="form-label fw-bold">Doctor</label>
        <select name="doctor" id="doctor" class="form-select" v-model="form.d_id" :disabled="!isProgressive">
          <option :value="user.d_id" v-for="user in userItems">{{ user.name }}</option>
        </select>
      </div>
      
      <div class="mb-3" v-if="!isProgressive && View =='patient'">
        <label class="form-label fw-bold">Doctor</label>
        <li class="list-group-item"> {{ userItems.name }}</li>
      </div>
      <div class="mb-3" v-if="!isProgressive && View =='doctor'">
        <label class="form-label fw-bold">Patient</label>
        <li class="list-group-item"> 
        <a :href="`http://localhost:5173/doctor/history/${form.p_id}`">
          {{ userItems.name }}
        </a>
        </li>
      </div>

      <div class="mb-3" v-if="!isProgressive">
        <label class="form-label fw-bold">Contact</label>
        <li class="list-group-item" v-if="userItems.email"> Email : {{ userItems.email }}</li>
        <li class="list-group-item" v-if="userItems.phone_no"> Phone Number: {{ userItems.phone_no }}</li>
      </div>

      <div class="mb-3" v-if="showDate && isProgressive">
        <label class="form-label fw-bold">Date</label>
        <select name="days" id="days" class="form-select" v-model="form.date" :disabled="!isProgressive">
          <option :value="day.date" v-for="day in dates" :disabled="!day['available']">{{ day.date }}</option>
        </select>
      </div>

      <div v-if="!isProgressive">
        <label class="form-label fw-bold">Date: {{ form['date'] }}</label>
      </div>
      
      <div class="mb-3" v-if="showSlot && View == 'patient' && !isHistorical && form['status'] == 'Booked'">
        <label class="form-label fw-bold">Time Slot</label>
        <select name="slot" id="slot" class="form-select" v-model="form.start_time">
          <option v-if="!form.date" disabled value="">Select a date first</option>
          <option :value="slot[0]" :key="slot[0]" v-for="slot in dates.find(obj => obj.date === form.date)?.slots" :disabled="!slot[1]">{{ slot[0] }}:00</option>
        </select>
      </div>

      <div v-if="!isProgressive && View =='doctor' || isHistorical || form['status'] == 'Completed'">
        <label class="form-label fw-bold">Time Slot {{ form.start_time }}:00</label>
      </div>

      <div class="mb-3" v-if="showSubmit && !isHistorical && View != 'doctor' && form['status'] != 'Completed'">
        <input type="submit" :value="isProgressive ? 'Book': 'Reschedule'" class="btn btn-primary form-control">
      </div>

    </form>

    <div v-if="!isProgressive && form['status'] == 'Completed' && View == 'doctor'">
      <form @submit.prevent="diagnose">
        <div v-if="View == 'patient'">
          <h4>Diagnosis: {{ form['diagnosis'] || 'Undecided' }}</h4>
        </div>
        <div v-if="View == 'doctor'">
          <h4 >Diagnosis:</h4>
          <input type="text" class="form-control" v-model="form['diagnosis']" required>
        </div>
        <button class="btn btn-primary form-control my-2" type="submit">Update</button>
        </form>
        <form @submit.prevent="addMed">
          <h4>Prescriptions</h4>
        <ul >
          <template v-if="prescriptions">
            <li class="list-group-item form-control" v-for="prescription in prescriptions"  :key="prescription.pr_id"> 
              {{ prescription.medicine }} 
              <button type="button" class="btn-close btn-sm" @click="remMed(prescription.pr_id)"></button>
            </li>
          </template>
          <span class="list-group-item" v-else>No prescriptions</span>
          <div class="input-group mt-2">
            <input type="text" class="form-control" placeholder="Medicine name" v-model="newMed">
            <button class="btn" type="submit">Add</button>
          </div>
        </ul>
        </form>

    </div>

    <div v-if="!isProgressive && !isHistorical && form['status'] == 'Booked' && View == 'doctor'">
      <button class="btn btn-primary form-control my-1" @click="markComplete">Mark as Complete</button>
    </div>
    <div class="mb-3" v-if="!isProgressive && !isHistorical && form['status'] == 'Booked'">
      <button class="btn btn-danger form-control my-1" @click="cancelAppointment">Cancel</button>
    </div>
    <div v-if="error" class="text-danger">{{ error }}</div>

</template>

