<script setup>
    import { useRouter } from 'vue-router'
    import sidebar from '@/components/sidebar.vue';
    import 'bootstrap/dist/css/bootstrap.min.css';
    const router = useRouter()
    const role = localStorage.getItem('role')
    const props = defineProps({
        navItems: Array
    })

</script>

<template>
    <div>
        <div class="row ">
            <sidebar :nav-items="props.navItems"></sidebar>
            <div class="col pt-4 px-5">
                <h1>Welcome {{role}}</h1>
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
