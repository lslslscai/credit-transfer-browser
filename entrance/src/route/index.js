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
    path: '/admin',
    component: admin
  },
  {
    path: '/school/:id',
    component: school
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes: routes
})

export default router
