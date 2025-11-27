<script setup>
    import { useRouter } from 'vue-router'
    import { onMounted } from 'vue'
    import 'bootstrap/dist/css/bootstrap.min.css';
    const router = useRouter()
    const user = JSON.parse(localStorage.getItem('user') || '{}')

    const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
    }
</script>

<template>
    <div>
        <div class="row ">
            <div class="col-2 pt-4">
                <h5>L'Hospital</h5>
                <ul class="nav flex-column">
                    <li class="nav-item py-2">
                        <RouterLink :to="{ name: 'adminDoctors'}">Doctors</RouterLink>
                    </li>
                    <li class="nav-item py-2">
                        <RouterLink :to="{ name: 'adminPatient'}">Patients</RouterLink>
                    </li>
                    <li class="nav-item py-2">
                        <RouterLink :to="{ name: 'adminDept'}">Departments</RouterLink>
                    </li>
                    <li class="nav-item py-2">
                        <RouterLink :to="{ name: 'adminAppointments'}">Appointments</RouterLink>
                    </li>
                </ul>
            </div>
            <div class="col pt-4 px-5">
                <h1>Welcome admin</h1>
                <RouterView />
            </div>
            
        </div>
    </div>
</template>

<style scoped>
h1{
    font-weight: 1000;
    font-size: 2.5rem; 
    position: relative;
}
</style>
