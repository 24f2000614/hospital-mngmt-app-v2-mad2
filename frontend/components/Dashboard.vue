<script setup>
import 'bootstrap/dist/css/bootstrap.min.css';
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
const data = ref([])
const error = ref(null)
const route = useRoute()
const searchQ = ref('');
const searchResults = ref({})
const searchView = ref(false)
const token = localStorage.getItem('token')

const props = defineProps({
    heading: String,
    endpoint: String,
    formpoint: String,
    newpoint: String,
    searchpoint: String
})

onMounted(()=>{
    fetchData()
})

const fetchData = async () => {
    try {
        data.value = []
        const req = await fetch(`http://127.0.0.1:5000/${props.endpoint}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`  
            },
        })

        if (!req.ok) throw new Error(req.message || 'Failed to fetch doctors')
        const res = await req.json()
        data.value = res
    } catch (e) {
        console.error(e)
        error.value = e.message
    }
    }

const search = async () => {
    if (!searchQ.value.trim()) return
    try{
        const req = await fetch(props.searchpoint, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ searchQ: searchQ.value })
        })
        const res = await req.json()
        searchResults.value = res
        console.log(res)
        searchView.value= true
        console.log(searchView.value)
    }catch (err) {
        console.log(err.message)
        error.value = err.message
    }


}


watch(() => props.endpoint, () => {
  fetchData()
}, {immediate:true})

const getId = (item) => {
  const key = Object.keys(item).find(k => k.includes('id'))
  return item[key]
}

const toggleSearchView = () => {
    searchView.value = false
    searchResults.value = []
    searchQ.value = ""
}

function handleError(message) {
    error.value = message
}


</script>

<template>
    <div class="container-fluid ">
        <div class="row">
            <div class="col-5">
                <h2>{{ heading }} ({{ data.length }})</h2>
                <div class="d-grid my-2" v-if="heading != `Patients` && heading != `Appointments`">
                    <RouterLink :to="{ name: props.newpoint }" class="btn btn-primary">Add New</RouterLink>
                </div>
                
                <div class="d-grid my-2">
                    <form @submit.prevent="search">
                        <input type="text" placeholder="Search" v-model="searchQ" class="form-control">
                    </form>
                    <button v-if="searchView" class="btn btn-secodary" @click="toggleSearchView">Clear Search</button>
                </div>

                        
                <ul class="list-group" v-if="searchView">
                    <li v-for="item in searchResults" :key="item[getId(item)]" class="list-group-item" >
                        <RouterLink :to="{name: `${props.formpoint}`, params: {id : getId(item)}}">{{ item.name }} - {{ item.description }}</RouterLink>
                    </li>
                </ul>
                <ul class="list-group" v-else>
                    <li v-for="item in data" :key="item[getId(item)]" class="list-group-item" >
                        <RouterLink :to="{name: `${props.formpoint}`, params: {id : getId(item)}}">{{ item.name }} - {{ item.description }}</RouterLink>
                    </li>
                </ul>


                <div v-if="error" class="text-danger">
                    {{ error }}
                </div>  
            </div>
            <div class="col-7">
                <RouterView :key="route.fullPath" @refresh="fetchData" @error="handleError"/>
            </div>
        </div>

    </div>
</template>