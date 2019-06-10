function disconnect_game(_this) {
    if (ws && ws.type == 'game') {
        ws.close()
    }
}

function connect_game() {
    if (ws) {
        ws.close()
    }

    ws = new WebSocket("ws://192.168.199.66:5007/game/gobang?accountNo=" + accountNo);
    ws.onopen = function (ev) {
        $('#game_body').show();
        cleanChat()
        onChat('连接游戏服务器成功');
        ws.type = 'game';
        $('#connect_game').hide();
        $('#disconnect_game').show();
        $('#exitGame').show();
        $('#nextGame').show();
        $('#refresh').show();
    }
    ws.onclose = function (ev) {
        onChat('已从游戏服务器断开');
        $('#game_body').hide();
        ws.type = '';
        $('#connect_game').show();
        $('#disconnect_game').hide();
        $('#exitGame').hide();
        $('#nextGame').hide();
        $('#refresh').hide();
    }
    ws.onmessage = function (ev) {
        var data = ''
        try {
            data = JSON.parse(ev.data)
        }
        catch (err) {
            onChat(ev.data)
        }
        if (!data) {
            return
        }
        console.log(data)
        try {
            switch (data['url']) {
                case '/game/S_C_playChess':
                    do_playChess_Player(data);
                    break
                case '/game/S_C_refreshChessBoard':
                    do_refreshChessBoard(data)
                    break
                case '/game/gameStart':
                    gameStart(data)
                    break
                case '/game/S_C_alertMsg':
                    alertMsg(data)
                    break
                case '/game/S_C_takeTurns':
                    takeTurns(data)
                    break
            }
        } catch (err) {
            console.log(err)
        }
    }
}

function disconnect_lobby(_this) {
    if (ws && ws.type == 'lobby') {
        ws.close()
    }
}

function connect_lobby(_this) {
    if (ws) {
        ws.close()
    }
    ws = new WebSocket("ws://192.168.199.66:5007/lobby?accountNo=" + accountNo);
    ws.onopen = function (ev) {
        $('#lobby_body').show();
        cleanChat()
        onChat('连接大厅服务器成功');
        ws.type = 'lobby';
        $('#connect_lobby').hide();
        $('#disconnect_lobby').show();
        $('#createRoom').show();
        $('#joinRandomGame').show();
    }
    ws.onclose = function (ev) {
        onChat('已从大厅服务器断开');
        $('#lobby_body').hide();
        ws.type = '';
        $('#connect_lobby').show();
        $('#disconnect_lobby').hide();
        $('#createRoom').hide();
        $('#joinRandomGame').hide();
    }
    ws.onmessage = function (ev) {
        var data = ''
        try {
            data = JSON.parse(ev.data)
        }
        catch (err) {
            onChat(ev.data)
        }
        if (!data) {
            return
        }
        console.log(data)
        try {
            switch (data['url']) {
                case '/game/S_C_alertMsg':
                    alertMsg(data)
                    break
            }
        } catch (err) {
            console.log(err)
        }
    }

}

window.onload = function () {

}

function sendMsg(str) {
    ws.send(JSON.stringify(str));
}

function alertMsg(data) {
    var msg = data['data']['msg']
    if (msg) {
        alert(msg)
    }
}

function takeTurns(data) {
    var chair = data['data']['chair']
    var accountNo = data['data']['accountNo']
    var roundNum = data['data']['roundNum']
    set_Info_actionPlayer(chair, accountNo)
    set_Info_gameRound(roundNum)
    curPlayer = accountNo
}

function gameStart(data) {
    // window.location.reload();
    connect_game();
}


function do_refreshChessBoard(data) {
    var allChessBoard = data['data']['chessBoard']

    if (!allChessBoard) {
        return
    }

    if (!isDrawChessBoard) {
        drawChessBoard()
    }

    for (var x = 0; x < allChessBoard.length; x++) {
        for (var y = 0; y < allChessBoard[x].length; y++) {
            play_type = allChessBoard[x][y]
            if (play_type == 1) {
                oneStep(x, y, true);
                chessBoard[x][y] = play_type;
            } else if (play_type == 2) {
                oneStep(x, y, false);
                chessBoard[x][y] = play_type;
            }
        }
    }
    var curGameCount = data['data']['curGameCount']
    set_Info_gameCount(curGameCount)
    var gameStage = data['data']['gameStage']
    set_Info_stage(gameStage)
    var roomId = data['data']['roomId']
    set_Info_roomid(roomId)

    var playerList = data['data']['playerList']
    for (var i = 0; i < playerList.length; i++) {
        playerInfo = playerList[i]
        play_type = playerInfo['play_type'] == 1 ? '黑色' : playerInfo['play_type'] == 2 ? '白色' : ''
        play_type_src = playerInfo['play_type'] == 1 ? `/static/img/black.jpg` : playerInfo['play_type'] == 2 ? `/static/img/white.jpg` : ''

        if (playerInfo['isme']) {
            $('#my_portrait .portrait_img_playType').attr('src', play_type_src)
            $('#my_portrait .portrait_span_accountNo').html(playerInfo['accountNo'])
        } else {
            $('#other_portrait .portrait_img_playType').attr('src', play_type_src)
            $('#other_portrait .portrait_span_accountNo').html(playerInfo['accountNo'])

        }
    }

}

function do_playChess_Player(data) {
    i = data['data']['x']
    j = data['data']['y']
    var play_type = data['data']['play_type']
    if (chessBoard[i][j] == 0) {
        if (play_type == 1) {
            oneStep(i, j, true);
        } else {
            oneStep(i, j, false);
        }
        chessBoard[i][j] = play_type;
    }
}