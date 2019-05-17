import Vue from 'vue'
import Router from 'vue-router'

const Login = () => import('@/page/login.vue');
const Room = () => import('@/page/room.vue')

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/room',
      name: 'Room',
      component: Room
    },
    {
      path: '/',
      redirect: '/login'
    }
  ]
})
