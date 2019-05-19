<template>
  <div class="main">
    <div class="roomList">
      <h1 class="title">房间列表</h1>
      <el-row :gutter="12">
        <el-col :span="8" v-for="item, index in room_list" :key="index">
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
      <ul>
        <li>
          <h2>世界：<i>哈哈</i><span>2019-5-10 18:08:30</span></h2>
          <p>聊天信息聊天信息</p>
        </li>
      </ul>
    </div>
    <div class="info">
      <el-input
        type="textarea"
        :rows="4"
        maxlength="77"
        placeholder="请输入内容"
        v-model="chat">
      </el-input>
      <div class="infoBtn">
        <el-button type="primary" style="border-radius: 0;">发送</el-button>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        room_list: [101, 201, 301, 201, 202, 203],
        chat: ''
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
