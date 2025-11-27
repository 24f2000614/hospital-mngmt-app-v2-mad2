import { createRouter, createWebHistory, useRoute } from 'vue-router'
import { getToken, isTokenValid, getUserRole } from '@/auth'
import { get } from '@/utils'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Dashboard from '../components/Dashboard.vue'
import WelcomeView from '../views/WelcomeView.vue'
import AdminView from '../views/AdminView.vue'
import Form from '../components/Form.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: WelcomeView,
      children: [
        {
          path: 'login',
          name: 'login',
          component: Login
        },
        {
          path: 'register',
          name: 'register',
          component: Register
        }
      ]
    },
    {
      path: "/admin",
      name: "adminHome",
      meta: { requiresAuth: true, role: 'Admin' },
      component: AdminView,
      children: [
        {
          path: "doctor",
          name: "adminDoctors",
          component: Dashboard,
          props: { heading: "Doctors", 
                  endpoint: "admin/doctors",
                  formpoint: "adminDoctorDetails",
                  newpoint: "adminNewDoctor",
                  searchpoint: "http://127.0.0.1:5000/admin/search/doctors"
                },
          meta: { requiresAuth: true, role: 'Admin' },
          children: [
            {
              path: ":id",
              name: "adminDoctorDetails",
              component: Form,
              props: { 
                heading: "Doctor Details",
                fields: [
                  { key: 'name', label: 'Doctor Name', type: 'text', required: true},
                  { key: 'email', label: 'Email', type: 'email', required: true,},
                  { key: 'description', label: 'Description', type: 'text', required: true, },
                  { key: 'dept_id', label: 'Department', type: 'select', required: true,
                    options: await get('http://127.0.0.1:5000/admin/dept')
                  },
                ],
                submitUrl: 'http://127.0.0.1:5000/admin/doctors',
                method: 'PUT',
                action: 'Delete'
                },
            },
            {
              path: "new",
              name: "adminNewDoctor",
              component: Form,
              props: { 
                heading: "Doctor Details",
                fields: [
                  { key: 'name', label: 'Doctor Name', type: 'text', required: true},
                  { key: 'email', label: 'Email', type: 'email', required: true,},
                  { key: 'description', label: 'Description', type: 'text', required: true, },
                  { key: 'dept_id', label: 'Department', type: 'select', required: true,
                    options: await get('http://127.0.0.1:5000/admin/dept')
                  },
                ],
                submitUrl: 'http://127.0.0.1:5000/admin/doctors',
                method: 'POST',
                },
            }
          ]
        },
        {
          path: "patient",
          name: "adminPatient",
          component: Dashboard,
          props: { heading: "Patients", 
                  endpoint: "admin/patients",
                  formpoint: "adminPatientDetails",
                  searchpoint: "http://127.0.0.1:5000/admin/search/patients"
                },
          meta: { requiresAuth: true, role: 'Admin' },
          children: [
            {
              path: ":id",
              name: "adminPatientDetails",
              component: Form,
              props: { 
                heading: "Patient Details",
                fields: [
                  { key: 'name', label: 'Patient Name', type: 'text', required: true},
                  { key: 'email', label: 'Email', type: 'email', required: true,},
                  { key: 'dob', label: 'Date of Birth', type: 'date', required: true,},
                  { key: 'phone_no', label: 'Phone number', type: 'text', required: true,},
                  { key: 'sex', label: 'Gender', type: 'radio', required: true, options: ['M', 'F']},
                ],
                submitUrl: 'http://127.0.0.1:5000/admin/patients/',
                method: 'PUT',
                action: 'Blacklist'
              }
            }
          ]
        },
        {
          path: "departments",
          name: "adminDept",
          component: Dashboard,
          props: { heading: "Departments", 
                  endpoint: "admin/dept",
                  formpoint: "adminDeptDetails",
                  newpoint: "adminNewDept",
                  searchpoint: "http://127.0.0.1:5000/admin/search/departments"
                },
          meta: { requiresAuth: true, role: 'Admin' },
          children: [
            {
              path: ":id",
              name: "adminDeptDetails",
              component: Form,
              props: { 
                heading: "Department Details",
                fields: [
                  { key: 'name', label: 'Dept Name', type: 'text', required: true},
                  { key: 'description', label: 'Description', type: 'text', required: true,},
                ],
                submitUrl: 'http://127.0.0.1:5000/admin/dept',
                method: 'PUT',
                action: 'Delete'
              }
            },
            {
              path: "new",
              name: "adminNewDept",
              component: Form,
              props: { 
                heading: "Department Details",
                fields: [
                  { key: 'name', label: 'Dept Name', type: 'text', required: true},
                  { key: 'description', label: 'Description', type: 'text', required: true,},
                ],
                submitUrl: 'http://127.0.0.1:5000/admin/dept',
                method: 'POST'
              }
            }
          ]
        },
              {
          path: "appointments",
          name: "adminAppointments",
          component: Dashboard,
          props: { heading: "Appointments", 
                  endpoint: "admin/appointments"
                },
          meta: { requiresAuth: true, role: 'Admin' },
        },
      ]
    }
  ],
})

router.beforeEach((to, from, next) => {
  const token = getToken()

  if (to.meta.requiresAuth) {
    if (!isTokenValid(token)) {
      return next('/login')
    }

    const role = getUserRole(token)
    if (to.meta.role && to.meta.role !== role) {
      return next('/login')
    }
  }

  next()
})

export default router
