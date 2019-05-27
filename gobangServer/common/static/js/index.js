var chessBoard = [];//棋盘
var isDrawChessBoard = false; //是否已画好棋盘
var curPlayer = '';//当前操作玩家
var accountNo = getUrlParam('accountNo')
var ws = '';

document.getElementById("createRoom").onclick = function () {
    sendMsg({"url": "/room/C_S_createGame"})
}
document.getElementById("joinRandomGame").onclick = function () {
    sendMsg({"url": "/room/C_S_joinGame", "params": {"isRandomRoom": true}})
}
document.getElementById("exitGame").onclick = function () {
    sendMsg({"url": "/game/C_S_exitGame"})
}
document.getElementById("nextGame").onclick = function () {
    sendMsg({"url": "/game/C_S_nextGame"})
}
document.getElementById("refresh").onclick = function () {
    window.location.reload();
}

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
        context.moveTo(40 + i * 30, 40);
        context.lineTo(40 + i * 30, 460);
        context.stroke();
        context.moveTo(40, 40 + i * 30);
        context.lineTo(460, 40 + i * 30);
        context.stroke();
    }
    isDrawChessBoard = true
}
//画棋子
var oneStep = function (i, j, me) {
    context.beginPath();
    context.arc(40 + i * 30, 40 + j * 30, 13, 0, 2 * Math.PI);// 画圆
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
    if (!isDrawChessBoard) {
        return
    }
    if (curPlayer != accountNo) {
        console.log('curPlayer'+curPlayer)
        console.log('accountNo'+accountNo)
        return
    }
    var x = e.offsetX;
    var y = e.offsetY;
    // if (x < 40 || y < 40 || x > 460 || y > 460) {
    // if (x < 30 || y < 30 || x > 470 || y > 470) {
    //     return
    // }


    var i = Math.floor((x-25) / 30);
    var j = Math.floor((y-25) / 30);
    console.log(x,y)
    console.log(i,j)

    if (i<0 || j<0||i>14||j>14){
        return
    }

    if (chessBoard[i][j] == 0) {
        sendMsg({"url": "/game/C_S_playChess", "params": {"x": i, "y": j}}
        )
    }
}

function onChat(msg) {
    var curDate = new Date();
    var curTime = curDate.toLocaleTimeString();
    $('.body_right').append(`<p>` + curTime + ` => ` + msg + `</p>`)
}


function set_Info_stage(stage) {
    var stageMap = {
        0: '等待开始',
        1: '游戏中',
        2: '结算中',
        3: '等待下局',
    }
    var stageMsg = stageMap[stage]
    if (stageMsg) {
        $('#game-info-stage p:nth-child(2)').html(stageMsg)
    }
}

function set_Info_roomid(roomid) {
    $('#game-info-roomid p:nth-child(2)').html(roomid)
}

function set_Info_gameCount(gameCount) {
    $('#game-info-gameCount p:nth-child(2)').html(gameCount)
}

function set_Info_gameRound(gameRound) {
    $('#game-info-gameRound p:nth-child(2)').html(gameRound)
}

function set_Info_actionPlayer(chair, accountNo) {
    var playerInfo = accountNo
    var chair = undefined
    if (chair != undefined) {
        playerInfo += `[` + chair + `]`
    }
    $('#game-info-actionPlayer p:nth-child(2)').html(playerInfo);
}