<template>
  <div id="main">
    <el-card :body-style="{ padding: '0px' }">
      <img src="../assets/logo.jpg"
           class="image">
      <div style="padding: 20px 14px;">
        <div class="demo-input-suffix">
          <el-row type="flex" align="middle">
            <el-col :span="3">
              账号：
            </el-col>
            <el-col :span="21">
              <el-input
                placeholder="请输入账号"
                v-model="username">
              </el-input>
            </el-col>
          </el-row>
          <el-row type="flex" justify="end">
            <el-col :span="4">
              <el-button type="success" round @click="login()">登录</el-button>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        username: ''
      }
    },
    created: function () {
      let _this = this;
      document.onkeydown = function (e) {
        let key = window.event.keyCode;
        if (key == 13) {
          _this.login();
        }
      };
    },
    methods: {
      login() {
        if (!this.username) {
          alert('账号不能为空！')
          return;
        }
        this.$router.push('/room')
      }
    }
  }
</script>

<style scoped>
  #main {
    position: fixed;
    top: 35%;
    left: 50%;
    width: 450px;
    margin-left: -225px;
  }
</style>
