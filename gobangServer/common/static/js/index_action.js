function createRoom() {
    sendMsg({"url": "/room/C_S_createGame"})
}

function joinRandomGame() {
    sendMsg({"url": "/room/C_S_joinGame", "params": {"isRandomRoom": true}})
}

function exitGame() {
    sendMsg({"url": "/game/C_S_exitGame"})
}

function readyStart() {
    sendMsg({"url": "/game/C_S_readyStart"})
}
function nextGame() {
    sendMsg({"url": "/game/C_S_nextGame"})
}

function refreshGame() {
    connect_game();
}