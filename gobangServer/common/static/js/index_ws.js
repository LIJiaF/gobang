window.onload = function () {
    ws = new WebSocket("ws://192.168.199.66:5007/game/gobang?accountNo=" + accountNo);
    // ws = new WebSocket("ws://192.168.199.66:5007/lobby?accountNo=" + accountNo);
    ws.onopen = function (ev) {
        onChat('连接成功');
    }
    ws.onmessage = function (ev) {
        try {
            data = JSON.parse(ev.data)
            console.log(data)
            switch (data['url']) {
                case '/game/S_C_playChess':
                    do_playChess_Player(data);
                    break
                case '/game/refreshChessBoard':
                    do_refreshChessBoard(data)
                    break
                case '/game/gameStart':
                    gameStart(data)
                    break
                case '/game/alertMsg':
                    alertMsg(data)
                    break
                case '/game/takeTurns':
                    takeTurns(data)
                    break
            }

        } catch (err) {
            console.log(ev.data)
            onChat(ev.data)
        }
    }


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
    window.location.reload();
}


function do_refreshChessBoard(data) {
    if (!isDrawChessBoard) {
        drawChessBoard()
    }

    var allChessBoard = data['data']['chessBoard']
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