function getUrlParam(paraName) {
    var url = document.location.toString();
    var arrObj = url.split("?");

    if (arrObj.length > 1) {
        var arrPara = arrObj[1].split("&");
        var arr;

        for (var i = 0; i < arrPara.length; i++) {
            arr = arrPara[i].split("=");

            if (arr != null && arr[0] == paraName) {
                return arr[1];
            }
        }
        return "";
    }
    else {
        return "";
    }
}

document.getElementById("createRoom").onclick = function () {
    sendMsg({"url": "/game/createGame"})
}
document.getElementById("joinRandomGame").onclick = function () {
    sendMsg({"url": "/game/joinRandomGame"})
}
document.getElementById("nextGame").onclick = function () {
    sendMsg({"url": "/game/nextGame"})
}
document.getElementById("refresh").onclick = function () {
    window.location.reload();
}

var chessBoard = [];//棋盘
var isDrawChessBoard = false; //是否已画好棋盘
function reset__chessBoard() {
    chessBoard = []
    for (var i = 0; i < 15; i++) {
        chessBoard[i] = [];
        for (var j = 0; j < 15; j++) {
            chessBoard[i][j] = 0;
        }
    }
}

reset__chessBoard()
var chess = document.getElementById("chess");
var context = chess.getContext('2d');

context.strokeStyle = '#bfbfbf'; //边框颜色


//绘画棋盘
var drawChessBoard = function () {
    for (var i = 0; i < 15; i++) {
        context.moveTo(15 + i * 30, 15);
        context.lineTo(15 + i * 30, 435);
        context.stroke();
        context.moveTo(15, 15 + i * 30);
        context.lineTo(435, 15 + i * 30);
        context.stroke();
    }
    isDrawChessBoard = true
}
//画棋子
var oneStep = function (i, j, me) {
    context.beginPath();
    context.arc(15 + i * 30, 15 + j * 30, 13, 0, 2 * Math.PI);// 画圆
    context.closePath();
    //渐变
    var gradient = context.createRadialGradient(15 + i * 30 + 2, 15 + j * 30 - 2, 13, 15 + i * 30 + 2, 15 + j * 30 - 2, 0);

    if (me) {
        gradient.addColorStop(0, '#0a0a0a');
        gradient.addColorStop(1, '#636766');
    } else {
        gradient.addColorStop(0, '#d1d1d1');
        gradient.addColorStop(1, '#f9f9f9');
    }
    context.fillStyle = gradient;
    context.fill();
}
//销毁棋子
var minusStep = function (i, j) {
    //擦除该圆
    context.clearRect((i) * 30, (j) * 30, 30, 30);

    // 重画该圆周围的格子
    context.beginPath();
    context.moveTo(15 + i * 30, j * 30);
    context.lineTo(15 + i * 30, j * 30 + 30);
    context.moveTo(i * 30, j * 30 + 15);
    context.lineTo((i + 1) * 30, j * 30 + 15);

    context.stroke();
}

// 我，下棋
chess.onclick = function (e) {
    var x = e.offsetX;
    var y = e.offsetY;
    var i = Math.floor(x / 30);
    var j = Math.floor(y / 30);
    _nowi = i;
    _nowj = j;
    if (chessBoard[i][j] == 0) {
        sendMsg({"url": "/game/playChess", "params": {"x": i, "y": j}}
        )
    }
}

function do_playChess_Player(data) {
    i = data['params']['x']
    j = data['params']['y']
    var play_type = data['params']['type']
    if (chessBoard[i][j] == 0) {
        if (play_type == 1) {
            oneStep(i, j, true);
        } else {
            oneStep(i, j, false);
        }
        chessBoard[i][j] = play_type;
    }
}

function do_refreshChessBoard(data) {
    if (!isDrawChessBoard) {
        drawChessBoard()
    }

    var allChessBoard = data['params']['chessBoard']
    for (var x = 0; x < allChessBoard.length; x++) {
        // console.log(allChessBoard[x])
        for (var y = 0; y < allChessBoard[x].length; y++) {
            play_type = allChessBoard[x][y]
            // console.log(play_type)
            if (play_type == 1) {
                oneStep(x, y, true);
                chessBoard[x][y] = play_type;
            } else if (play_type == 2) {
                oneStep(x, y, false);
                chessBoard[x][y] = play_type;
            }
        }
    }
    var curGameCount = data['params']['curGameCount']
    document.getElementById("roomInfo").innerText = '第' + curGameCount + '局'
}

function gameStart(data) {
    window.location.reload();
}

function alertMsg(data) {
    var msg = data['params']['msg']
    if (msg) {
        alert(msg)
    }
}


var accountNo = getUrlParam('accountNo')
var ws = '';
window.onload = function () {
    // drawChessBoard(); // 画棋盘

    ws = new WebSocket("ws://192.168.199.66:5006/game/gobang?accountNo=" + accountNo);
    ws.onopen = function (ev) {
        // ws.send(JSON.stringify({'name': 'winslen001'}));
    }
    ws.onmessage = function (ev) {
        try {
            data = JSON.parse(ev.data)
            console.log(data)
            switch (data['url']) {
                case '/game/playChess':
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
            }

        } catch (err) {
            console.log(ev.data)
        }
    }


}

function sendMsg(str) {
    ws.send(JSON.stringify(str));
}

