import { createRouter, createWebHashHistory } from "vue-router"
import helloWorld from '../components/HelloWorld.vue'
import admin from '../components/admin.vue'
import school from '../components/school.vue'


const routes = [
  {
    path: '/',
    component: helloWorld
  },
  {
    path: '/admin/:ip',
    component: admin
  },
  {
    path: '/school/:id/:ip',
    component: school
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes: routes
})

export default router
