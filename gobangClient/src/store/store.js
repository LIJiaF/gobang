import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations.js'

Vue.use(Vuex);

const state = {
  // url: 'ws://127.0.0.1:5006',
  url: 'ws://192.168.199.66:5006',
  room_ws: null,
  main_ws: null,
}

export default new Vuex.Store({
  state,
  mutations
})
