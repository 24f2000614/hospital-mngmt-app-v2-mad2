<script setup>
    import { useRouter } from 'vue-router'
    const router = useRouter()
    const props = defineProps({
        navItems: Array
    })
    const logout = () => {
        localStorage.removeItem('token')
        localStorage.removeItem('role')
        router.push({name:"login"})
    }
</script>

<template>
    <div class="col-2 pt-4">
        <h5>L'Hospital</h5>
        <ul class="nav flex-column">
            <li class="nav-item py-2" v-for="item in props.navItems">
                <RouterLink :to="item.id ? { name: item.route } : { name: item.route }">{{ item.name }}</RouterLink>
            </li>
            <li class="nav-item py-2">
                <button @click="logout" class="btn text-danger btn-link m-0 p-0">Logout</button>
            </li>
        </ul>
    </div>
</template>