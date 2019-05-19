<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
  export default {
    name: 'App'
  }
</script>

<style>
  * {
    margin: 0;
    padding: 0;
    font-size: 14px;
    text-decoration: none;
    outline: none;
    list-style: none;
  }

  .el-row {
    padding: 5px 0;
  }

  .el-card {
    cursor: pointer;
  }

  .el-card__body {
    font-size: 35px;
    font-weight: bold;
  }

  .el-textarea__inner {
    resize: none;
    border: none;
  }
</style>
