import Vue from 'vue'
import Axios from 'axios'
import Router from 'vue-router'

import store from '../store/store.js';

const Login = () => import('@/page/login.vue');
const Room = () => import('@/page/room.vue');
const Main = () => import('@/page/main.vue');

Vue.prototype.$axios = Axios;
Vue.use(Router);

const router = new Router({
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
});

router.beforeEach((to, from, next) => {
  let username = sessionStorage.getItem('username');
  // 跳转到登录页面或已经连接WebSocket
  if (to.path === '/login' || store.state.room_ws) {
    next();
  } else {
    // 其他页面，存在用户名则重连
    if (username) {
      Axios.get('/api/lobby/login?accountNo=' + username)
        .then((res) => {
          let data = res.data;
          if (!data.code) {
            let url = store.state.url + data.data.ws_address;
            let ws = new WebSocket(url);
            store.commit('ROOMWS', ws);
          }
          next();
        })
        .catch((err) => {
          console.log(err);
          next({
            path: '/login',
            query: {redirect: to.fullPath}
          });
        });
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      });
    }
  }
});

export default router;
