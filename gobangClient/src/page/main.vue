<template>
  <div class="main">
    <h1 class="title">{{ title }}</h1>
    <canvas ref="chess" width="500px" height="500px" @click="play"></canvas>
    <div class="footer">
      <el-button type="primary" round @click="reload">重新开始</el-button>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        'title': '--益智五子棋--',               // 标题显示内容
        'canvas': null,                         // 画布
        'url': 'ws://127.0.0.1:5006/game/001',  // webSocket地址
        'ws': null,                             // webSocket对象
        'over': false,                          // 是否结束
        'me': true,                             // 是否到我
        'myWinArr': [],                         // 我赢的统计数组
        'computerWinArr': [],                   // 计算机赢的统计数组
        'chressBord': [],                       // 棋盘数组
      }
    },
    created() {
      this.initChressBord();
      this.$nextTick(() => {
        let chess = this.$refs.chess;
        this.canvas = chess.getContext('2d');
        this.canvas.strokeStyle = '#bfbfbf'; //边框颜色
        this.drawChessBoard(); // 画棋盘
        this.initWebSocket();
      });
    },
    computed: {
      // 赢法数组
      wins() {
        let wins = [];
        for (let i = 0; i < 15; i++) {
          wins[i] = [];
          for (let j = 0; j < 15; j++) {
            wins[i][j] = [];
          }
        }
        return wins;
      },
      // 赢法总数
      total() {
        let total = 0;
        //横线赢法
        for (let i = 0; i < 15; i++) {
          for (let j = 0; j < 11; j++) {
            for (let k = 0; k < 5; k++) {
              this.wins[i][j + k][total] = true;
            }
            total++;
          }
        }

        //竖线赢法
        for (let i = 0; i < 15; i++) {
          for (let j = 0; j < 11; j++) {
            for (let k = 0; k < 5; k++) {
              this.wins[j + k][i][total] = true;
            }
            total++;
          }
        }

        //正斜线赢法
        for (let i = 0; i < 11; i++) {
          for (let j = 0; j < 11; j++) {
            for (let k = 0; k < 5; k++) {
              this.wins[i + k][j + k][total] = true;
            }
            total++;
          }
        }

        //反斜线赢法
        for (let i = 0; i < 11; i++) {
          for (let j = 14; j > 3; j--) {
            for (let k = 0; k < 5; k++) {
              this.wins[i + k][j - k][total] = true;
            }
            total++;
          }
        }

        for (let i = 0; i < total; i++) {
          this.myWinArr[i] = 0;
          this.computerWinArr[i] = 0;
        }

        return total;
      }
    },
    methods: {
      initChressBord() {
        let chressList = [];
        for (let i = 0; i < 15; i++) {
          chressList[i] = [];
          for (let j = 0; j < 15; j++) {
            chressList[i][j] = 0;
          }
        }
        this.chressBord = chressList;
      },
      initWebSocket() {
        this.ws = new WebSocket(this.url);
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
          for (let k = 0; k < this.total; k++) { // 将可能赢的情况都加1
            if (this.wins[i][j][k]) {
              this.myWinArr[k]++;
              this.computerWinArr[k] = 6;  // 这个位置对方不可能赢了
              if (this.myWinArr[k] == 5) {
                this.title = '恭喜，你赢了！';
                this.over = true;
              }
            }
          }
          if (!this.over) {
            this.me = !this.me;
            this.computerAI();
          }
        }
      },
      doPlayChessRobot(data) {
        let i = data['x']
        let j = data['y']
        let chair = data['chair']
        if (this.chressBord[i][j] == 0) {
          this.oneStep(i, j, false);
          this.chressBord[i][j] = chair;    // 机器人占据位置

          for (let k = 0; k < this.total; k++) {
            if (this.wins[i][j][k]) {
              this.computerWinArr[k]++;
              this.myWinArr[k] = 6;    // 这个位置对方不可能赢了
              if (this.computerWinArr[k] == 5) {
                this.title = 'o(╯□╰)o，计算机赢了，继续加油哦！';
                this.over = true;
              }
            }
          }

          if (!this.over) {
            this.me = !this.me;
          }
        }
      },
      computerAI() {
        let myScore = [];
        let computerScore = [];
        let max = 0;
        let u = 0, v = 0;
        for (let i = 0; i < 15; i++) {
          myScore[i] = [];
          computerScore[i] = [];
          for (let j = 0; j < 15; j++) {
            myScore[i][j] = 0;
            computerScore[i][j] = 0;
          }
        }
        for (let i = 0; i < 15; i++) {
          for (let j = 0; j < 15; j++) {
            if (this.chressBord[i][j] == 0) {
              for (let k = 0; k < this.total; k++) {
                if (this.wins[i][j][k]) {
                  if (this.myWinArr[k] == 1) {
                    myScore[i][j] += 200;
                  } else if (this.myWinArr[k] == 2) {
                    myScore[i][j] += 400;
                  } else if (this.myWinArr[k] == 3) {
                    myScore[i][j] += 2000;
                  } else if (this.myWinArr[k] == 4) {
                    myScore[i][j] += 10000;
                  }

                  if (this.computerWinArr[k] == 1) {
                    computerScore[i][j] += 220;
                  } else if (this.computerWinArr[k] == 2) {
                    computerScore[i][j] += 420;
                  } else if (this.computerWinArr[k] == 3) {
                    computerScore[i][j] += 2100;
                  } else if (this.computerWinArr[k] == 4) {
                    computerScore[i][j] += 20000;
                  }
                }
              }

              if (myScore[i][j] > max) {
                max = myScore[i][j];
                u = i;
                v = j;
              } else if (myScore[i][j] == max) {
                if (computerScore[i][j] > computerScore[u][v]) {
                  u = i;
                  v = j;
                }
              }

              if (computerScore[i][j] > max) {
                max = computerScore[i][j];
                u = i;
                v = j;
              } else if (computerScore[i][j] == max) {
                if (myScore[i][j] > myScore[u][v]) {
                  u = i;
                  v = j;
                }
              }

            }
          }
        }

        this.sendMsg({
          'x': u,
          'y': v,
          'chair': 2,
          'action': 'Robot_Play_Chess',
        });
      },
      drawChessBoard() {
        for (let i = 0; i < 15; i++) {
          let canvas = this.canvas;
          canvas.moveTo(40 + i * 30, 40);
          canvas.lineTo(40 + i * 30, 460);
          canvas.stroke();
          canvas.moveTo(40, 40 + i * 30);
          canvas.lineTo(460, 40 + i * 30);
          canvas.stroke();
        }
      },
      play(e) {
        if (this.over || !this.me) {
          return;
        }

        let x = e.offsetX;
        let y = e.offsetY;
        let i = Math.floor(x / 30) - 1;
        let j = Math.floor(y / 30) - 1;

        console.log(x, y, i, j);

        if (!this.chressBord[i][j]) {
          this.sendMsg({
            'x': i,
            'y': j,
            'chair': 1,
            'action': 'Player_Play_Chess'
          });
        }
      },
      reload() {
        // 初始化数据
        this.initChressBord();
        this.title = '--益智五子棋--';
        this.over = false;
        this.me = true;
        this.myWinArr = [];
        this.computerWinArr = [];

        //  重新渲染棋盘
        let canvas = this.canvas;
        canvas.fillStyle = "#fff";
        canvas.beginPath();
        canvas.fillRect(0, 0, 500, 500);
        canvas.closePath();
        this.drawChessBoard();
      },
      oneStep(i, j, me) {
        let canvas = this.canvas;
        canvas.beginPath();
        canvas.arc(40 + i * 30, 40 + j * 30, 13, 0, 2 * Math.PI);// 画圆
        canvas.closePath();
        //渐变
        let gradient = canvas.createRadialGradient(40 + i * 30 + 2, 40 + j * 30 - 2, 13, 40 + i * 30 + 2, 40 + j * 30 - 2, 0);

        if (me) {
          gradient.addColorStop(0, '#0a0a0a');
          gradient.addColorStop(1, '#636766');
        } else {
          gradient.addColorStop(0, '#d1d1d1');
          gradient.addColorStop(1, '#f9f9f9');
        }
        canvas.fillStyle = gradient;
        canvas.fill();
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
