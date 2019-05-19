import Vue from 'vue'
import Router from 'vue-router'

const Login = () => import('@/page/login.vue');
const Room = () => import('@/page/room.vue');
const Main = () => import('@/page/main.vue');

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
      path: '/main/:id',
      name: 'Main',
      component: Main
    },
    {
      path: '/',
      redirect: '/login'
    }
  ]
})
