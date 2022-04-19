import { createRouter, createWebHashHistory } from "vue-router"
import Test from '../components/test.vue'

import StuHelloWorld from '../views/student_view/StuHelloWorld.vue'
import StuLogin from '../views/student_view/login.vue'
import StuHomePage from '../components/student/StuHomePage.vue'
import SelectLesson from '../views/student_view/select_lesson/select_lesson.vue'
import Score from '../views/student_view/score_page/score_page.vue'

import TeaHelloWorld from '../views/teacher_view/TeaHelloWorld.vue'
import TeaLogin from '../views/teacher_view/login.vue'
import TeaHomePage from '../components/teacher/TeaHomePage.vue'
import TeaStudentAdmin from '../views/teacher_view/student_page/student_admin.vue'
import TeaStudentAdd from '../views/teacher_view/student_page/student_add.vue'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    component: StuLogin
  },
  {
    path: '/home',
    name: 'StuHomePage',
    component: StuHomePage,
    children: [
      {
        path: '',
        component: StuHelloWorld
      },
      {
        path: '/personal_page',
        component: Test
      },
      {
        path: '/personal_page/score',
        name: 'Score',
        component: Score
      },
      {
        path: '/course',
        component: Test
      },
      {
        path: '/course/select/',
        name: 'SelectLesson',
        component: SelectLesson
      },
      {
        path: '/course/select/exterior/',
        component: Test
      },
      {
        path: '/credit_transfer',
        name: 'Test',
        component: Test
      },
      {
        path: '/credit_transfer/states',
        name: 'Test',
        component: Test
      },
    ]
  },
  {
    path: '/admin',
    component: TeaLogin
  },
  {
    path: '/admin/main',
    component: TeaHomePage,
    children: [
      {
        path: '',
        component: TeaHelloWorld
      },
      {
        path: 'course',
        component: Test
      },
      {
        path: 'course/add',
        component: Test
      },
      {
        path: 'course/adjust',
        component: Test
      },
      {
        path: 'student',
        component: TeaStudentAdmin
      },
      {
        path: 'student/add',
        component: TeaStudentAdd
      },
      {
        path: 'student/adjust/:id',
        component: Test
      },
      {
        path: 'credit_transfer',
        component: Test,
        children:[
          {
            path: ':id',
            component: Test
          }
        ]
      },
    ]
  },
  {
    path: '/404',
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes: routes
})


router.beforeEach((to, from, next) => {
  if (to.path.includes("admin")) {
    if (!document.cookie.includes("Tealogin=")
      && to.path != "/admin") {
      next({
        path: '/admin'
      })
    }
    else if (to.path != "/")
      next()
  }
  else {
    if (!document.cookie.includes("Stulogin=")
      && to.path != "/login") {
      next({
        path: '/login'
      })
    }
    else if (to.path != "/")
      next()
  }
})
export default router
