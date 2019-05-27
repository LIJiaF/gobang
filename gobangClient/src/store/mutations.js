const ROOMWS = 'ROOMWS';
const GAMEWS = 'GAMEWS';

export default {
  [ROOMWS](state, room_ws) {
    state.room_ws = room_ws;
  },
  [GAMEWS](state, game_ws) {
    state.game_ws = game_ws;
  }
}
