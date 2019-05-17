<template>
  <div class="main">
    <div class="roomList">
      <h1 class="title">房间列表</h1>
      <el-row :gutter="12">
        <el-col :span="8" v-for="item, index in room_list" :key="index">
          <el-card shadow="hover">
            {{ item }}
          </el-card>
        </el-col>
      </el-row>
    </div>
    <div class="info">
      <div class="chat">

      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        room_list: [101, 201, 301, 201, 202, 203]
      }
    }
  }
</script>

<style scoped>
  .roomList, .info {
    float: left;
    width: 50%;
    padding: 10px;
    text-align: center;
    box-sizing: border-box;
  }

  .title {
    padding: 10px 0;
    text-align: center;
    font-size: 18px;
    font-weight: normal;
  }

  .info {
    padding: 20px;
    box-sizing: border-box;
  }

  .chat{
    width: 100%;
    height:200px;
    border:1px solid red;
  }
</style>
