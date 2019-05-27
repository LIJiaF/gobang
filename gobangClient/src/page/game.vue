<template>
  <div class="main">
    <div class="info">
      <p class="time">30</p>
      <p>房间号：20190527</p>
      <p>游戏状态：等待中...</p>
      <p>当前局数：3</p>
      <p>当前操作人：LiJiaF</p>
      <div class="btnGroup">
        <el-button type="primary" round @click="reload">重新开始</el-button>
        <el-button type="primary" round @click="reload">退出房间</el-button>
      </div>
    </div>
    <div class="chessboard">
      <h1 class="title">{{ title }}</h1>
      <div class="userInfo" style="margin-bottom: -30px;">
        <img src="../assets/white.jpg"/>
        <p>玩家：LiJiaF</p>
      </div>
      <canvas ref="chess" width="500px" height="500px" @click="play"></canvas>
      <div class="userInfo" style="margin-top: -46px;">
        <img src="../assets/black.jpg"/>
        <p>玩家：LiJiaF</p>
      </div>
    </div>
    <div class="chat">
      <h1 class="chatTitle">聊天窗口</h1>
      <div class="chatList" ref="chatList">
        <ul>
          <li v-for="(info, index) in infoList" :key="index">
            <h2>{{info.accountNo}}<span>{{info.time}}</span></h2>
            <p>{{info.msg}}</p>
          </li>
        </ul>
      </div>
      <div class="msg">
        <el-input
          type="textarea"
          :rows="4"
          maxlength="77"
          placeholder="请输入内容"
          v-model="info">
        </el-input>
        <div class="btn">
          <el-button type="primary" style="border-radius: 0;" @click="sendChat">发送</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {mapState} from 'vuex'

  export default {
    data() {
      return {
        'title': '--益智五子棋--',               // 标题显示内容
        'canvas': null,                         // 画布
        'over': false,                          // 是否结束
        'me': true,                             // 是否到我
        'myWinArr': [],                         // 我赢的统计数组
        'computerWinArr': [],                   // 计算机赢的统计数组
        'chressBord': [],                       // 棋盘数组
        'infoList': [],
        'info': '',
      }
    },
    created() {
      this.initChressBord();
      this.$nextTick(() => {
        // 聊天窗口显示最新消息
        let chatList = this.$refs.chatList;
        chatList.scrollTop = chatList.scrollHeight;

        let chess = this.$refs.chess;
        this.canvas = chess.getContext('2d');
        this.canvas.strokeStyle = '#bfbfbf'; //边框颜色
        this.drawChessBoard(); // 画棋盘
        this.initWebSocket()
      });
    },
    updated() {
      this.$nextTick(() => {
        // 聊天窗口显示最新消息
        let chatList = this.$refs.chatList;
        chatList.scrollTop = chatList.scrollHeight;
      });
    },
    computed: {
      ...mapState([
        'game_ws'
      ]),
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
        this.game_ws.onopen = this.webSocketOnOpen;
        this.game_ws.onerror = this.webSocketOnError;
        this.game_ws.onmessage = this.webSocketOnMessage;
        this.game_ws.onclose = this.webSocketOnClose;
      },
      webSocketOnOpen() {
        console.log('GAME WebSocket连接成功');
      },
      webSocketOnError() {
        console.log("GAME WebSocket连接发生错误");
      },
      webSocketOnMessage(ev) {
        let data = ev.data;
        try {
          data = JSON.parse(data);
          switch (data['action']) {
            case 'Player_Play_Chess':
              this.doPlayChessPlayer(data);
              break;
            case 'Robot_Play_Chess':
              this.doPlayChessRobot(data);
              break;
          }
        } catch (err) {
          console.log(data);
        }
      },
      webSocketOnClose() {
        console.log('main WebSocket关闭成功');
      },
      sendMsg(dict) {
        this.game_ws.send(JSON.stringify(dict));
      },
      sendChat() {
        let json_data = {'accountNo': 'LiJiaF', 'time': '2019-05-27 21:43:00', 'msg': this.info}
        this.infoList.push(json_data)
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
        // let canvas = this.canvas;
        // canvas.fillStyle = "#fff";
        // canvas.beginPath();
        // canvas.fillRect(0, 0, 500, 500);
        // canvas.closePath();
        // this.drawChessBoard();
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
    position: relative;
  }

  .info {
    position: absolute;
    left: 15px;
  }

  .info p {
    font-size: 18px;
    padding: 10px 0;
  }

  .info .time {
    margin: 15px auto;
    width: 80px;
    height: 60px;
    line-height: 60px;
    font-size: 30px;
    color: #fff;
    border: 1px solid #409EFF;
    background: #409EFF;
    border-radius: 50%;
    text-align: center;
  }

  .btnGroup{
    margin: 30px 0;
    width:100%;
    text-align: center;
  }

  .btnGroup button{
    display: block;
    text-align: center;
    margin: 10px auto;
  }

  .chessboard {
    width: 500px;
    margin: 20px auto;
  }

  .userInfo {
    overflow: hidden;
  }

  .userInfo img {
    margin-left: 37px;
    margin-top: 15px;
    float: left;
    width: 60px;
  }

  .userInfo p {
    margin-right: 37px;
    margin-top: 15px;
    float: right;
    height: 60px;
    line-height: 60px;
  }

  .chessboard .title {
    text-align: center;
    font-size: 18px;
  }

  .chessboard .footer {
    text-align: center;
  }

  .chat {
    position: absolute;
    right: 0;
    top: 0;
    margin: 10px;
  }

  .chatTitle {
    font-weight: normal;
    text-align: center;
    background: #409EFF;
    height: 40px;
    line-height: 40px;
    color: #fff;
    border: 1px solid #409EFF;
  }

  .chatList {
    width: 250px;
    height: 435px;
    border: 1px solid #ccc;
    border-radius: 0 0 5px 5px;
    overflow: auto;
  }

  .chatList li {
    padding: 10px;
  }

  .chatList span {
    float: right;
    color: #999;
    font-size: 12px;
  }

  .chatList p {
    padding: 7px 0;
    border-bottom: 1px solid #ccc;
  }

  .msg {
    position: relative;
    margin-top: 10px;
    border: 1px solid #ccc;
    box-sizing: border-box;
  }

  .btn {
    position: absolute;
    bottom: -1px;
    right: -1px;
  }
</style>
