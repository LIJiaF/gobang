<template>
  <div class="main">
    <h1 class="title">--益智五子棋--</h1>
    <canvas ref="chess" width="500px" height="500px" @click="play"></canvas>
    <div class="footer">
      <el-button type="primary" round>重新开始</el-button>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        'context': null,  // 画布
        'ws': null,       // websocket
        'over': false,    // 是否结束
        'me': true,       // 是否到我
      }
    },
    created() {
      this.$nextTick(() => {
        let chess = this.$refs.chess;
        this.context = chess.getContext('2d');
        this.context.strokeStyle = '#bfbfbf'; //边框颜色
        this.drawChessBoard(); // 画棋盘
      });
      this.initWebSocket()
    },
    computed: {
      chressBord() {
        let chressList = [];
        for (let i = 0; i < 15; i++) {
          chressList[i] = [];
          for (let j = 0; j < 15; j++) {
            chressList[i][j] = 0;
          }
        }
        return chressList;
      },
      count() {
        let count = 0;
        //横线赢法
        for (var i = 0; i < 15; i++) {
          for (var j = 0; j < 11; j++) {
            for (var k = 0; k < 5; k++) {
              wins[i][j + k][count] = true;
            }
            count++;
          }
        }

        //竖线赢法
        for (var i = 0; i < 15; i++) {
          for (var j = 0; j < 11; j++) {
            for (var k = 0; k < 5; k++) {
              wins[j + k][i][count] = true;
            }
            count++;
          }
        }

        //正斜线赢法
        for (var i = 0; i < 11; i++) {
          for (var j = 0; j < 11; j++) {
            for (var k = 0; k < 5; k++) {
              wins[i + k][j + k][count] = true;
            }
            count++;
          }
        }

        //反斜线赢法
        for (var i = 0; i < 11; i++) {
          for (var j = 14; j > 3; j--) {
            for (var k = 0; k < 5; k++) {
              wins[i + k][j - k][count] = true;
            }
            count++;
          }
        }

        return count;
      }
    },
    methods: {
      initWebSocket() {
        let url = 'ws://127.0.0.1:5006/game/001';
        this.ws = new WebSocket(url);
        this.ws.onopen = this.webSocketOnOpen;
        this.ws.onerror = this.webSocketOnError;
        this.ws.onmessage = this.webSocketOnMessage;
      },
      webSocketOnOpen() {
        this.ws.send(JSON.stringify({'name': 'LiJiaF'}));
      },
      webSocketOnError() {
        console.log("WebSocket连接发生错误");
      },
      webSocketOnMessage(ev) {
        let data = JSON.parse(ev.data);
        console.log(JSON.parse(ev.data));
        switch (data['action']) {
          case 'Player_Play_Chess':
            this.doPlayChessPlayer(data);
            break;
          case 'Robot_Play_Chess':
            this.doPlayChessRobot(data);
            break;
        }
      },
      sendMsg(dict) {
        this.ws.send(JSON.stringify(dict));
      },
      doPlayChessPlayer(data) {
        let i = data['x'];
        let j = data['y'];
        let chair = data['chair'];
        if (!this.chressBord[i][j]) {
          this.oneStep(i, j, this.me);
          this.chressBord[i][j] = chair; //我，已占位置
          console.log(this.count);
          for (let k = 0; k < this.count; k++) { // 将可能赢的情况都加1
            if (wins[i][j][k]) {
              myWin[k]++;
              _compWin[k] = computerWin[k];
              computerWin[k] = 6;//这个位置对方不可能赢了
              if (myWin[k] == 5) {
                resultTxt.innerHTML = '恭喜，你赢了！';
                this.over = true;
              }
            }
          }
          if (!this.over) {
            this.me = !this.me;
            computerAI();
          }
        }
      },
      doPlayChessRobot() {
      },
      oneStep(i, j, me) {
        let context = this.context;
        context.beginPath();
        context.arc(40 + i * 30, 40 + j * 30, 13, 0, 2 * Math.PI);// 画圆
        context.closePath();
        //渐变
        let gradient = context.createRadialGradient(40 + i * 30 + 2, 40 + j * 30 - 2, 13, 40 + i * 30 + 2, 40 + j * 30 - 2, 0);

        if (me) {
          gradient.addColorStop(0, '#0a0a0a');
          gradient.addColorStop(1, '#636766');
        } else {
          gradient.addColorStop(0, '#d1d1d1');
          gradient.addColorStop(1, '#f9f9f9');
        }
        context.fillStyle = gradient;
        context.fill();
      },
      drawChessBoard() {
        for (let i = 0; i < 15; i++) {
          let context = this.context;
          context.moveTo(40 + i * 30, 40);
          context.lineTo(40 + i * 30, 460);
          context.stroke();
          context.moveTo(40, 40 + i * 30);
          context.lineTo(460, 40 + i * 30);
          context.stroke();
        }
      },
      play(e) {
        if (this.over || !this.me) {
          return;
        }

        let x = e.offsetX;
        let y = e.offsetY;
        let i = Math.floor(x / 30);
        let j = Math.floor(y / 30);

        if (!this.chressBord[i][j]) {
          this.sendMsg({
            'x': i,
            'y': j,
            'chair': 1,
            'action': 'Player_Play_Chess'
          });
        }
      }
    }
  }
</script>

<style scoped>
  .main {
    width: 500px;
    margin: 20px auto;
  }

  .title {
    text-align: center;
    font-size: 18px;
  }

  .footer {
    text-align: center;
  }
</style>
