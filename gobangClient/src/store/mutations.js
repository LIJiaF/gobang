const ROOMWS = 'ROOMWS';
const MAINWS = 'MAINWS';

export default {
  [ROOMWS](state, room_ws) {
    state.room_ws = room_ws;
  },
  [MAINWS](state, main_ws) {
    state.main_ws = main_ws;
  }
}
