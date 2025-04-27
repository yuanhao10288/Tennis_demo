<template>
  <div class="home">
    <div class="center-rectangle">
      <div class="header-frame">
        <div class="header-left">
          <img src="../assets/tennis.svg" alt="网球" class="icon" />
          <h1 class="title">慧球灵析——智能网球训练系统</h1>
        </div>
      </div>
      <!-- 按钮组 -->
      <div class="button-group">
        <!-- 战术分析按钮 -->
        <router-link to="/analysis">
          <button class="action-btn">战术分析</button>
        </router-link>
        <!-- 启动捡球按钮 -->
        <button @click="startBallPickup" class="action-btn">启动捡球</button>
      </div>
      <!-- 开始运动和停止运动按钮 -->
      <div class="control-buttons">
        <button @click="startExercise" class="control-btn start-btn">开始运动</button>
        <button @click="stopExercise" class="control-btn stop-btn">停止运动</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home {
  text-align: center;
  /* 添加背景图片样式 */
  background-image: url('../assets/background.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  /* 隐藏默认背景颜色 */
  background-color: transparent;
  /* 设置高度以确保背景图片可见 */
  min-height: 100vh;
  opacity: 0.79;
  position: relative;
}

.center-rectangle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 65%;
  height: 58%;
  background-color: rgba(255, 255, 255, 0.5);
  z-index: 1;
  border-radius: 65px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  justify-content: flex-start; /* 内容顶部对齐 */
  padding: 20px;
  gap: 30px; /* 添加元素之间的间距 */
}

/* 跟 Home.vue 一致的标题框样式 */
.header-frame {
  top:0;
  width: 100%;
  position: relative;
  display: flex;
  margin-top: 20px;
  align-items: center;
  justify-content: center;
  /* 如需更随意形状可启用下面这一行，注释或删除 border-radius */
  /* clip-path: polygon(5% 0, 100% 10%, 95% 100%, 0 90%); */
}

.header-left {
  display: flex;
  align-items: center;
}

.header-left .icon {
  width: 48px;
  height: 48px;
  margin-right: 10px;
}

.header-left .title {
  font-size: 60px;
  font-weight: bold;
  color: black;
  top: 40px;
}

/* 按钮组样式 */
.button-group {
  display: flex;
  flex-direction: column;
  width: 30%;
  gap: 30px;
}

.action-btn {
  margin-top: 20px;
  background-color: white;
  border: 1px solid white;
  color: black;
  font-weight: bold;
  font-size: 40px;
  cursor: pointer;
  padding: 10px;
  width: 100%;
  border-radius: 37px;
}

/* 控制按钮样式 */
.control-buttons {
  display: flex;
  justify-content: space-between;
  width: 70%;
  margin-top: 50px;
  gap: 400px;
}

.control-btn {
  background-color: white;
  border: 1px solid white;
  color: black;
  font-weight: bold;
  font-size: 40px;
  cursor: pointer;
  border-radius: 37px;
  padding: 10px;
  width: 45%;
}
</style>