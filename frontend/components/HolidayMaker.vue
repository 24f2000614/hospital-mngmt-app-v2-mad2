<script setup>
    import { ref, onMounted } from 'vue'
    import { get } from '@/utils'
    import { getToken } from '@/auth'
    const dates = ref(null)
    const token = getToken()
    const holidayList = ref([])
    const props = defineProps({
        d_id: String,
    })
    const holidayToBe = ref(null)
    onMounted(async ()=>{
        dates.value = await get(`http://127.0.0.1:5000/patient/doc-availability/${props.d_id}`)
        for (const item of dates.value){
            let holidayBool = true
            if(!item.available) {
                holidayBool=false
                continue
            }
            const day = item.date
            for (const slot of item.slots) {
                if (!slot[1]) holidayBool = false
            }
            const pair = [day, holidayBool]
            holidayList.value.push(pair)
        }
    })
    const BookHoliday = async() => {
        if (!holidayToBe.value) return
        const req = await fetch(`http://127.0.0.1:5000/doctor/holiday/${props.d_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({"date": holidayToBe.value})
        })
        if (req.ok){
            alert("Holiday Booked successfully!")
        }
    }
</script>

<template>
    <h2>Book your Holiday!</h2>

    <label for="holiday" class="form-label fw-bold">Choose date</label>
    <select v-model="holidayToBe" class="form-select form-control mb-3" id="holiday" name="holiday">
        <option :value="day[0]" v-for="day in holidayList" :disabled="!day[1]">{{ day[0] }}</option>
    </select>

    <div v-if="holidayToBe">
        <button type="submit" class="btn btn-primary mb-3" @click="BookHoliday">Book Holiday</button>
    </div>
</template>