import { createRouter, createWebHistory } from 'vue-router'
import { getToken, isTokenValid, getUserRole, getUserId } from '@/auth'
import { get } from '@/utils'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Dashboard from '../components/Dashboard.vue'
import WelcomeView from '../views/WelcomeView.vue'
import UserView from '../views/UserView.vue'
import Form from '../components/Form.vue'
import Appointment from '../components/Appointment.vue'
import HolidayMaker from '@/components/HolidayMaker.vue'

const token = getToken()
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
      component: UserView,
      props: {
        navItems: [
          {name:"Doctors", route:"adminDoctors"},
          {name:"Patients", route:"adminPatient"},
          {name:"Department", route:"adminDept"},
          {name:"Appointments", route:"adminAppointments"},
        ]
      },
      children: [
        {
          path: "doctor",
          name: "adminDoctors",
          component: Dashboard,
          props: { heading: "Doctors", 
                  endpoint: "admin/doctors",
                  formpoint: "adminDoctorDetails",
                  newpoint: "adminNewDoctor",
                  searchpoint: "admin/search/doctors",
                  primary_fields: ['name', 'description']
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
                    options: getUserRole(token) === 'Admin' ? await get('http://127.0.0.1:5000/admin/dept'): ''
                  },
                ],
                submitUrl: 'admin/doctors',
                method: 'PUT',
                action: 'Delete',
                static: false
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
                    options: getUserRole(token) === 'Admin' ? await get('http://127.0.0.1:5000/admin/dept'): ''
                  },
                ],
                submitUrl: 'admin/doctors',
                method: 'POST',
                static: false
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
                  searchpoint: "admin/search/patients",
                  primary_fields: ['name', 'email']
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
                  { key: 'address', label: 'Address', type: 'textarea', required: true},
                ],
                submitUrl: 'admin/patients',
                method: 'PUT',
                action: 'Blacklist',
                static: false
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
                  searchpoint: "admin/search/departments",
                  primary_fields: ['name', 'description']
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
                submitUrl: 'admin/dept',
                method: 'PUT',
                static:false
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
                submitUrl: 'admin/dept',
                method: 'POST',
                static: false
              }
            }
          ]
        },
        {
          path: '/appointments',
          name: 'adminAppointments',
          component: Dashboard,
          props: {
            heading: "Appointments",
            endpoint: "admin/appointments",
            formpoint: "adminAppDetails",
            primary_fields: ['start_time', 'status'],
          },
          children: [
            {
              path: ":id",
              name: "adminAppDetails",
              component: Appointment,
              props: {
                heading: "Appointment Details",
                isProgressive: false,
                View: 'admin',
                isHistorical: false
              }
            }
          ]
        }
      ]
    },
    {
      path: "/patient",
      name: "patientHome",
      meta: { requiresAuth: true, role: 'Patient'},
      component: UserView,
      props: {
        navItems: [
          {name:"Appointments", route:"patientAppointments"},
          {name:"Department", route:"patientDept"},
          {name: "Profile", route:"patientProfile"},
          {name:"Book", route:"patientBookings"},
          {name:"History", route:"patientHistory"},
        ]
      },
      children:[
        {
          path: 'department',
          name: "patientDept",
          component: Dashboard,
          props: {
            heading: "Departments",
            endpoint: "patient/dept",
            formpoint: "deptDoctorList",
            searchpoint: "patient/search-dept",
            primary_fields: ['name', 'description']
          },
          children: [
            {
              path: ":id",
              name: "deptDoctorList",
              component: Dashboard,
              props: {
                heading: "List of doctors",
                endpoint: "patient/dept",
                formpoint: "",
                searchpoint: "patient/search-doctor",
                primary: "dept",
                primary_fields: ['name', 'description'],
                secondary: "doctor_list",
                secondary_fields: ['name', 'description'],
              }
            }
          ]
        },
        {
          path: 'profile',
          name: "patientProfile",
          component: Form,
          props:{
            heading: "Patient Details",
            fields: [
              { key: 'name', label: 'Patient Name', type: 'text', required: true},
              { key: 'email', label: 'Email', type: 'email', required: true,},
              { key: 'dob', label: 'Date of Birth', type: 'date', required: true,},
              { key: 'phone_no', label: 'Phone number', type: 'text', required: true,},
              { key: 'sex', label: 'Gender', type: 'radio', required: true, options: ['M', 'F']},
              { key: 'address', label: 'Address', type: 'textarea', required: true},
            ],
            submitUrl: "patient/profile",
            method: 'PUT',
            static: false,
            id: getUserId(token)}
        },
        {
          path: "booking",
          name: "patientBookings",
          component: Appointment,
          props: {
            heading: "Book Appointment",
            isProgressive: true,
            View: 'patient'
          }
        },
        {
          path: "appointment",
          name: "patientAppointments",
          component: Dashboard,
          props: {
            heading: "Appointments",
            endpoint: "patient/appointments",
            formpoint: "patientAppDetails",
            primary_fields: ['start_time', 'status']
          },
          children: [
            {
              path: ":id",
              name: "patientAppDetails",
              component: Appointment,
              props: {
                heading: "Appointment Details",
                isProgressive: false,
                View: 'patient',
                isHistorical: false
              }
            }
          ]
        },
        {
          path: 'history',
          name: 'patientHistory',
          component: Dashboard,
          props: {
            heading: "History",
            endpoint: "patient/appointments",
            formpoint: "deptHistDetails",
            searchpoint: "patient/search-dept",
            primary_fields: ['start_time', 'status'],
          },
          children: [
            {
              path: ":id",
              name: "deptHistDetails",
              component: Appointment,
              props: {
                heading: "Appointment Details",
                isProgressive: false,
                View: 'patient',
                isHistorical: true
              }
            }
          ]
        }
      ]
    },
    {
      path: "/doctor",
      name: "doctorHome",
      meta: {requiresAuth:true, role: 'Doctor'},
      component: UserView,
      props: {
        navItems: [
          {name: "Appointments", route: "doctorAppointments"},
          {name: "Profile", route: "doctorProfile"},
          {name: "HolidayMaker", route: "holidayMaker"},
        ]
      },
      children:[
        {
          path: "appointment",
          name: "doctorAppointments",
          component: Dashboard,
          props: {
            heading: "Appointments",
            endpoint: "doctor/appointments",
            formpoint: "doctorAppDetails",
            primary_fields: ['start_time', 'status']
          },
          children: [
            {
              path: ":id",
              name: "doctorAppDetails",
              component: Appointment,
              props: {
                heading: "Appointment Details",
                isProgressive: false,
                View: 'doctor',
                isHistorical: false
              }
            }
          ]
        },
        {
          path: "profile",
          name: "doctorProfile",
          component: Form,
          props:{
            heading: "Doctor Details",
            fields: [
              { key: 'name', label: 'Doctor Name', type: 'text', required: true},
              { key: 'email', label: 'Email', type: 'email', required: true,},
              { key: 'description', label: 'Description', type: 'text', required: true, },
              { key: 'dept_id', label: 'Department', type: 'select', required: true,
                // options: getUserRole(token) === 'Admin' ? await get('http://127.0.0.1:5000/admin/dept'): ''
              },
            ],
            submitUrl: 'doctor/profile',
            static: true,
            id: getUserId(token)
          }
        },
        {
          path: "history/:p_id",
          name: "docHistory",
        },
        {
          path: "/holiday",
          name: "holidayMaker",
          component: HolidayMaker,
          props: {
            d_id: getUserId(token)
          }
        }
      ]
    }
  ]
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
