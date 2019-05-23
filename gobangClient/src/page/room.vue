<template>
  <div class="main">
    <div class="roomList">
      <h1 class="title">房间列表</h1>
      <el-row :gutter="12">
        <el-col :span="8" v-for="item, index in roomList" :key="index">
          <router-link :to="'/main/'+item">
            <el-card shadow="hover" style="margin: 10px 0;">
              {{ item }}
            </el-card>
          </router-link>
        </el-col>
      </el-row>
    </div>
    <div class="chat">
      <h1>世界</h1>
      <div class="chatList">
        <ul id="chatList">
          <li v-for="(chat, index) in chatList" :key="index">
            <h2>世界：<i>{{ chat.accountNo }}</i><span>{{chat.date}}</span></h2>
            <p>{{chat.msg}}</p>
          </li>
        </ul>
      </div>
    </div>
    <div class="info">
      <el-input
        type="textarea"
        :rows="4"
        maxlength="77"
        placeholder="请输入内容"
        v-model="info">
      </el-input>
      <div class="infoBtn">
        <el-button type="primary" style="border-radius: 0;" @click="sendMsg()">发送</el-button>
      </div>
    </div>
  </div>
</template>

<script>
  import {mapState} from 'vuex'
  import mapping from '@/config/mapping.js'

  export default {
    data() {
      return {
        roomList: [101, 201, 301, 201, 202, 203],
        chatList: [],
        info: ''
      }
    },
    created() {
      this.initWebSocket();
      this.$nextTick(function () {
        let ul = document.getElementById('chatList');
        window.onscroll = function(){
          console.log(ul.scrollTop);
          console.log(ul.scrollHeight);
        };
      });
    },
    updated() {
      this.$nextTick(function () {
        let ul = document.getElementById('chatList');
        ul.scrollTop = ul.scrollHeight;
      });
    },
    computed: {
      ...mapState([
        'room_ws'
      ])
    },
    methods: {
      initWebSocket() {
        this.room_ws.onopen = this.webSocketOnOpen;
        this.room_ws.onerror = this.webSocketOnError;
        this.room_ws.onmessage = this.webSocketOnMessage;
      },
      webSocketOnOpen() {
        console.log('WebSocket连接成功');
      },
      webSocketOnError() {
        console.log("WebSocket连接发生错误");
      },
      webSocketOnMessage(ev) {
        let data = ev.data;
        try {
          data = JSON.parse(data);
          if (mapping.hasOwnProperty(data.url)) {
            let {sender: {accountNo}, senderTime: date, msg} = data.data;
            let method = mapping[data.url];
            eval(`this.${method}('${accountNo}', '${date}', '${msg}')`);
          }
        } catch (err) {
          console.log(ev.data);
        }
      },
      sendMsg() {
        let json_data = {"url": "/chat/sendMsg_allOnline", "params": {"msg": this.info}};
        this.room_ws.send(JSON.stringify(json_data));
      },
      room_chat(accountNo, date, msg) {
        // this.info = '';
        this.chatList.push({'accountNo': accountNo, 'date': date, 'msg': msg});
      }
    }
  }
</script>

<style scoped>
  .roomList {
    float: left;
    width: 50%;
    padding: 10px;
    text-align: center;
    box-sizing: border-box;
  }

  .title {
    padding: 33px 0;
    text-align: center;
    font-size: 18px;
    font-weight: normal;
    background: #F6F6F6 url("../assets/title.jpg") no-repeat center center;
  }

  .chat {
    position: fixed;
    top: 10px;
    right: 10px;
    left: 51%;
    bottom: 120px;
    border: 1px solid #ccc;
  }

  .chatList {
    position: absolute;
    width: 100%;
    top: 45px;
    bottom: 0;
    overflow: auto;
  }

  .chat h1 {
    font-size: 18px;
    padding: 10px;
    text-align: center;
    font-weight: bold;
    border-bottom: 1px solid #ccc;
    color: #fff;
    background: #409EFF;
  }

  .chat li {
    text-align: left;
    padding: 10px;
  }

  .chat span {
    float: right;
    color: #999;
    font-size: 12px;
  }

  .chat p {
    padding: 7px 0;
    border-bottom: 1px solid #ccc;
  }

  .info {
    position: fixed;
    right: 10px;
    left: 51%;
    bottom: 10px;
    border: 1px solid #ccc;
    box-sizing: border-box;
  }

  .infoBtn {
    position: absolute;
    bottom: 0;
    right: 0;
  }
</style>
