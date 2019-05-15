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
                v-model="input2">
              </el-input>
            </el-col>
          </el-row>
          <el-row type="flex" justify="end">
            <el-col :span="4">
              <el-button type="success" round>登录</el-button>
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
        msg: 'Welcome to Your Vue.js App'
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

  .el-row {
    padding: 5px 0;
  }
</style>
