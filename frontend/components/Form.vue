<script setup>
import { reactive, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { get } from "@/utils";
const props = defineProps({
    heading: String,
    fields: Array,
    submitUrl: String,
    method: { type: String, default: "POST" },
    action: String,
    static: Boolean,
    id: String
});

const route = useRoute()
const router = useRouter()
const emit = defineEmits(['refresh', 'error'])
const form = reactive({});
const id = route.params.id
const token = localStorage.getItem("token");
let initialData = null

onMounted(async () => {
    try {
        if (id || props.id){
            initialData = await get(`http://127.0.0.1:5000/${props.submitUrl}/${id || props.id}`);
            Object.assign(form, initialData);
            console.log(form)
        }
    } catch (err) {
        console.error("Failed to fetch initial data:", err);
        emit('error', err)
    }
});

if(id || props.id) {
    watch(() => route.params.id, async () => {
        initialData = await get(`http://127.0.0.1:5000/${props.submitUrl}/${route.params.id}`);
        Object.assign(form, initialData);
    })
}


const handleSubmit = async () => {
    const url = id ? `http://127.0.0.1:5000/${props.submitUrl}/${route.params.id}` : `http://127.0.0.1:5000/${props.submitUrl}`;
    await fetch(url, {
        method: props.method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(form)
    });
    if (props.method === 'POST'){
        for (const key in form) {
            form[key] = ''; 
        }
    }
  emit('refresh')
};

const handleDelete = async () => {
    const url = `http://127.0.0.1:5000/${props.submitUrl}/${route.params.id}`
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
</script>

<template>
    <h1>{{ props.heading }}</h1>
    <form @submit.prevent="handleSubmit">

    <div v-for="field in fields" :key="field.key" class="mb-3">

        <label class="form-label fw-bold">{{ field.label }}</label>
        <div v-if="!props.static">
            <input 
                v-if="['text','password','email','number','date'].includes(field.type)"
                v-model="form[field.key]"
                :type="field.type"
                class="form-control"
                :required="field.required"
                />
                
            <select 
                v-else-if="field.type === 'select'"
                v-model="form[field.key]"
                class="form-select"
                :required="field.required"
                >
                <option v-for="opt in field.options" :value="opt.dept_id" >
                    {{ opt.name }}
                </option>
            </select>
            
            <textarea 
                v-else-if="field.type === 'textarea'" 
                v-model="form[field.key]"
                class="form-control"
                :required="field.required"
            ></textarea>

            <input v-else v-model="form[field.key]" class="form-control"/>

        </div>
        <div v-else>
            <li class="list-group-item">{{ form[field.key] }}</li>
        </div>
    </div>
    <button class="btn btn-primary my-1" type="submit" v-if="!staticx">
        {{ method === "POST" ? "Create" : "Update" }}
    </button>

  </form>
  <button v-if="props.action && !static" class="btn btn-secondary my-1" @click="handleDelete">
        {{ props.action }}
    </button>
</template>
