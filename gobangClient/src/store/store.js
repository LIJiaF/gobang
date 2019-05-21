import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations.js'

Vue.use(Vuex);

const state = {
  room_ws: null,
}

export default new Vuex.Store({
  state,
  mutations
})
