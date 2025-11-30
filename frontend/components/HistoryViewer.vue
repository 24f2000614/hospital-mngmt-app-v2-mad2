<script setup>
    import { onBeforeMount, watch, ref } from 'vue';
    import { useRoute } from 'vue-router';
    import { get } from '@/utils';
    const props = defineProps({
        heading: String
    })
    const route = useRoute()
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const hmm = ref({})
    const appointment = ref(null)
    const dateObj = ref(null)
    const doctor = ref(null)
    const dept = ref(null)
    const patient = ref(null)
    const prescriptions = ref(null)
    const dateStr = ref("")
    const slot = ref(null)

    const fetchData = async() => {
        const a_id = route.params.a_id || route.params.id
        hmm.value = await get(`http://127.0.0.1:5000/admin/history/${a_id}`)
        appointment.value = hmm.value["appointment"]
        dateObj.value = new Date(appointment.value['start_time'])
        dateStr.value = `${days[dateObj.value.getDay()]} ${dateObj.value.getUTCDate()}-${dateObj.value.getMonth()}-${dateObj.value.getFullYear()}`
        slot.value = dateObj.value.getUTCHours() 
        doctor.value = hmm.value["doctor"]
        dept.value = await get(`http://127.0.0.1:5000/admin/dept/${doctor.value.d_id}`)
        patient.value = hmm.value["patient"]
        prescriptions.value = hmm.value["prescriptions"]
    }
    watch(() => route.params.a_id || route.params.id, fetchData)
    onBeforeMount(fetchData)
</script>

<template>
    <h2>{{props.heading}}</h2>
    <div class="mb-3">
        <label class="form-label fw-bold">Department</label>
        <li class="list-group-item">{{ dept['name'] }}</li>
    </div>
    <div class="mb-3">
        <label class="form-label fw-bold">Doctor</label>
        <li class="list-group-item">{{ doctor['name'] }}</li>
        <li class="list-group-item">{{ doctor['email'] }}</li>
    </div>
    <div class="mb-3">
        <label class="form-label fw-bold">Patient</label>
        <li class="list-group-item">{{ patient['name'] }}</li>
    </div>
    <div class="mb-3">
        <label class="form-label fw-bold">Patient Contact</label>
        <li class="list-group-item"> Email : {{ patient['email'] }}</li>
        <li class="list-group-item"> Phone Number: {{ patient['phone_no'] }} </li>
    </div>
    <div>
        <label class="form-label fw-bold">Date: {{ dateStr }}</label>
    </div>
    <div>
        <label class="form-label fw-bold">Time Slot: {{ slot }}:00</label>
    </div>
    <template v-if="prescriptions">
        <label class="form-label fw-bold">Prescriptions</label>
        <li class="list-group-item form-control" v-for="prescription in prescriptions"  :key="prescription.pr_id"> 
            {{ prescription['medicine'] }}
        </li>
    </template>
</template>