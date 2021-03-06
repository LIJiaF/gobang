<template>
  <div class="main">
    <div class="room_list">
      <h1 class="title">房间列表</h1>
      <div class="room">
        <el-row :gutter="12">
          <el-col :span="8" v-for="(item, index) in roomList" :key="index" @click.native="joinRoom(item.roomId)">
            <el-card shadow="hover" style="margin: 10px 0;">
              <h1>房间号：{{ item.roomId }}</h1>
              <p>房主：{{ item.owner }}</p>
              <p>在线人数：{{ item.playerCount }}</p>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
    <div class="btnGroup">
      <el-row>
        <el-col :span="12">
          <el-button type="primary" round @click="createRoom">创建房间</el-button>
        </el-col>
        <el-col :span="12">
          <el-button type="primary" round>加入房间</el-button>
        </el-col>
      </el-row>
    </div>
    <div class="chat">
      <h1>世界</h1>
      <div class="chatList" id="chatList">
        <ul>
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
        <el-button type="primary" style="border-radius: 0;" @click="sendChat">发送</el-button>
      </div>
    </div>
  </div>
</template>

<script>
  import {mapState, mapMutations} from 'vuex'
  import mapping from '../config/mapping.js'

  export default {
    data() {
      return {
        roomList: [],
        chatList: [],
        info: ''
      }
    },
    created() {
      // 初始化WebSocket
      this.initWebSocket();
      // 获取房间列表
      this.getRoomList();

      // 显示最新聊天信息
      this.$nextTick(function () {
        let chatList = document.getElementById('chatList');
        chatList.scrollTop = chatList.scrollHeight;
      });
    },
    updated() {
      // 显示最新聊天信息
      this.$nextTick(function () {
        let chatList = document.getElementById('chatList');
        chatList.scrollTop = chatList.scrollHeight;
      });
    },
    computed: {
      ...mapState([
        'url',
        'room_ws',
        'game_ws'
      ])
    },
    methods: {
      ...mapMutations([
        'ROOMWS',
        'GAMEWS'
      ]),
      initWebSocket() {
        this.room_ws.onopen = this.webSocketOnOpen;
        this.room_ws.onerror = this.webSocketOnError;
        this.room_ws.onmessage = this.webSocketOnMessage;
        this.room_ws.onclose = this.webSocketOnClose;
      },
      webSocketOnOpen() {
        console.log('ROOM WebSocket连接成功');
      },
      webSocketOnError() {
        console.log("ROOM WebSocket连接发生错误");
      },
      webSocketOnMessage(ev) {
        let data = ev.data;
        try {
          data = JSON.parse(data);
          if (mapping.hasOwnProperty(data.url)) {
            let method = mapping[data.url];
            let context = JSON.stringify(data);
            eval(`this.${method}('${context}')`);
          }
        } catch (err) {
          console.log(data);
        }
      },
      webSocketOnClose() {
        console.log('ROOM WebSocket关闭成功');
      },
      sendMsg(data) {
        this.room_ws.send(JSON.stringify(data));
      },
      // 发送聊天信息
      sendChat() {
        let json_data = {"url": "/chat/C_S_sendMsg_allOnline", "params": {"msg": this.info}};
        this.sendMsg(json_data);
      },
      sendChatCall(data) {
        let {sender: {accountNo}, senderTime: date, msg} = JSON.parse(data).data;
        this.chatList.push({'accountNo': accountNo, 'date': date, 'msg': msg});
        this.info = '';
      },
      // 获取房间列表
      getRoomList() {
        let json_data = {"url": "/room/C_S_getRoomList"};
        this.sendMsg(json_data);
      },
      getRoomListCall(data) {
        let res = JSON.parse(data);
        if (!res.code) {
          this.roomList.push(...res.data);
        }
        console.log('房间列表：' + res.msg);
      },
      // 创建房间
      createRoom() {
        let json_data = {"url": "/room/C_S_createGame", "params": {"isJoinIn": false}};
        this.sendMsg(json_data);
      },
      createRoomCall(data) {
        let res = JSON.parse(data);
        if (!res.code) {
          this.roomList.push(...res.data);
        }
        console.log('创建房间：' + res.msg);
      },
      // 加入房间
      joinRoom(roomId) {
        let json_data = {"url": "/room/C_S_joinGame", "params": {"roomId": roomId}};
        this.sendMsg(json_data);
      },
      joinRoomCall(data) {
        let res = JSON.parse(data);
        console.log('加入房间：' + res.msg);
        this.$router.push('/game');
      }
    }
  }
</script>

<style scoped>
  .room_list {
    position: fixed;
    bottom: 90px;
    top: 0;
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

  .room {
    height: 90%;
    border-bottom: 1px solid #ccc;
  }

  .btnGroup {
    position: fixed;
    width: 50%;
    bottom: 20px;
    text-align: center;
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
