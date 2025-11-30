<script setup>
import 'bootstrap/dist/css/bootstrap.min.css';
import { ref, onMounted, watch } from 'vue'
import { getUserId } from '@/auth';
import { useRoute } from 'vue-router'
const data = ref([])
const primaryData = ref(null)
const secondaryData = ref(null)
const error = ref(null)
const route = useRoute()
const id = route.params.id
const searchQ = ref('');
const searchResults = ref({})
const searchView = ref(false)
const token = localStorage.getItem('token')
const p_id = getUserId(token)

const emit = defineEmits(['error'])

const props = defineProps({
    heading: String,
    endpoint: String,
    formpoint: String,
    newpoint: String,
    searchpoint: String,
    primary: String,
    primary_fields: Array,
    secondary_fields: Array,
    secondary: String, 
    status: String,
    isAid: Boolean,
    export: String
})

onMounted( async ()=>{
    fetchData()
})

const fetchData = async () => {
    try{
    if(!id){
    const reqMain = await fetch(`http://127.0.0.1:5000/${props.endpoint}`, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })
        data.value = await reqMain.json()
    }else{
            const reqSub = await fetch(`http://127.0.0.1:5000/${props.endpoint}/${id}`, {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            })
            const res = await reqSub.json()
            primaryData.value = res[props.primary] || null
            secondaryData.value = res[props.secondary] || null
        } 
    } catch(err){
        error.value = err.message
    }
}

const search = async () => {
    if (!searchQ.value.trim()) return
    try{
        if (id) {
            const req = await fetch(`http://127.0.0.1:5000/${props.searchpoint}`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ searchQ: searchQ.value, dept_id:id  })
            })
            const res = await req.json()
            searchResults.value = res
        }
        else{
            const req = await fetch(`http://127.0.0.1:5000/${props.searchpoint}`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ searchQ: searchQ.value })
            })
            const res = await req.json()
            searchResults.value = res
        }
        searchView.value= true
    }catch (err) {
        error.value = err.message
    }


}
const makeText = (item, fields) => {
    return fields.map(f => item[f]).join(" - ")  
}

watch(() => route.fullPath, () => {
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
            <div class="col-5" v-if="secondaryData === null">
                <h2>{{ heading }} ({{ data.length }})</h2>
                <a v-if="props.export" :href="`${props.export}/${p_id}`">Click Here to send history csv to mail</a>
                <div class="d-grid my-2" v-if="props.newpoint">
                    <RouterLink :to="{ name: props.newpoint }" class="btn btn-primary">Add New</RouterLink>
                </div>
                
                <div class="d-grid my-2" v-if="props.searchpoint">
                    <form @submit.prevent="search">
                        <input type="text" placeholder="Search" v-model="searchQ" class="form-control">
                    </form>
                    <button v-if="searchView" class="btn btn-secodary" @click="toggleSearchView">Clear Search</button>
                </div>

                        
                <ul class="list-group" v-if="searchView">
                    <li v-for="item in searchResults" :key="item[getId(item)]" class="list-group-item" >
                        <RouterLink :to="{name: `${props.formpoint}`, params: {id : getId(item)}}">{{ makeText(item, props.primary_fields) }}</RouterLink>
                    </li>
                </ul>
                <ul class="list-group" v-else>
                    <li v-for="item in data" :key="item[getId(item)]" class="list-group-item" >
                        <RouterLink :to="{name: `${props.formpoint}`, params: {id : getId(item)}}">{{ makeText(item, props.primary_fields) }}</RouterLink>
                    </li>
                </ul>


                <div v-if="error" class="text-danger">
                    {{ error }}
                </div>  
            </div>
            <div v-else>
                <h3>{{ heading }}</h3>
                <div>
                    <h5>{{ makeText(primaryData, props.primary_fields) }}</h5>
                </div>
                
                <div class="d-grid my-2" v-if="props.searchpoint">
                    <form @submit.prevent="search">
                        <input type="text" placeholder="Search" v-model="searchQ" class="form-control">
                    </form>
                    <button v-if="searchView" class="btn btn-clear" @click="toggleSearchView">Clear Search</button>
                </div>
                <ul class="list-group" v-if="searchView">
                    <li v-for="item in searchResults" :key="item[getId(item)]" class="list-group-item" >
                        <RouterLink :to="{name: `${props.formpoint}`, params: {id : getId(item)}}">{{ makeText(item, props.primary_fields) }}</RouterLink>
                    </li>
                </ul>
                <ul class="list-group" v-else>
                    <li v-for="item in secondaryData" class="list-group-item"  v-if="secondaryData.length && !formpoint">
                        {{ makeText(item, props.secondary_fields) }}
                    </li>
                        <li v-for="item in secondaryData" class="list-group-item"  v-if="secondaryData.length && formpoint && !isAid">
                        <RouterLink :to = "{name: `${props.formpoint}`, params: {id : getId(item)}}">{{ makeText(item, props.secondary_fields) }}</RouterLink>
                    </li>
                    <li v-for="item in secondaryData" class="list-group-item"  v-if="secondaryData.length && formpoint && isAid">
                        <RouterLink :to = "{name: `${props.formpoint}`, params: {id, a_id : getId(item)}}">{{ makeText(item, props.secondary_fields) }}</RouterLink>
                    </li>
                </ul>
            </div>
            <div class="col-7">
                <RouterView :key="route.fullPath" @refresh="fetchData" @error="handleError"/>
            </div>
        </div>
        
    </div>
</template>