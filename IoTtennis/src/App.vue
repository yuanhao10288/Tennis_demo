<template>
  <div id="app">
    <!-- 路由出口，显示当前路由对应的组件 -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* 可加全局样式 */
/* 全局背景色 */
html, body, #app {
  margin: 0;
  padding: 0;
  min-height: 100vh;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>
