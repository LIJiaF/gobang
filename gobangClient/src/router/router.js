import Vue from 'vue'
import Axios from 'axios'
import Router from 'vue-router'

import store from '../store/store.js';

const Login = () => import('@/page/login.vue');
const Room = () => import('@/page/room.vue');
const Game = () => import('@/page/game.vue');

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
      path: '/game',
      name: 'Game',
      component: Game
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
  if (to.path === '/login' || store.state.room_ws || store.state.game_ws) {
    next();
  } else {
    // 其他页面，存在用户名则重连
    if (username) {
      if (to.path === '/room') {
        try {
          var url = store.state.url + '/lobby?accountNo=' + username;
          var ws = new WebSocket(url);
          store.commit('ROOMWS', ws);
        } catch (err) {
          console.log('socket连接失败：' + url);
          next({
            path: '/login',
            query: {redirect: to.fullPath}
          });
        } finally {
          next();
        }
      } else if (to.path === '/game') {
        try {
          var url = store.state.url + '/game/gobang?accountNo=' + username;
          var ws = new WebSocket(url);
          store.commit('GAMEWS', ws);
        } catch (err) {
          console.log('socket连接失败：' + url);
          next({
            path: '/login',
            query: {redirect: to.fullPath}
          });
        } finally {
          next();
        }
      } else {
        next({
          path: '/login'
        });
      }
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      });
    }
  }
});

export default router;
