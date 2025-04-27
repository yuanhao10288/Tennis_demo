<template>
    <div class="analysis">
      <!-- 标题区 -->
      <div class="header-frame">
        <div class="header-left">
          <img src="../assets/tennis.svg" alt="网球" class="icon" />
          <h1 class="title">慧球灵析——智能网球训练系统</h1>
        </div>
        <router-link to="/">
          <button class="action-btn">返回首页</button>
        </router-link>
      </div>
  
       <!-- 内容区：三等分左右中布局 -->
      <div class="content-area">
        <div class="column left">
          <div class="box left-top">
            <div class="weather-top">
              <img src="../assets/sun.svg" alt="太阳" class="weather-icon" />
              <div class="weather-info">
                <div class="temperature">25℃</div>
                <div class="condition">晴天</div>
              </div>
            </div>
            <div class="weather-bottom">
              <div class="wind">
                <div class="label">风速</div>
                <div class="value">东南风 3级</div>
              </div>
              <div class="humidity">
                <div class="label">湿度</div>
                <div class="value">53%</div>
              </div>
            </div>
          </div>
          <!-- 左区下方矩形：热力图 -->
          <div class="box left-bottom">
            <div class="heatmap-title">球员运动轨迹热力图</div>
            <img src="../assets/heatmap.png" alt="热力图" class="heatmap-image" />
          </div>
        </div>
        <div class="column center">
          <div class="box center-box">
            <div class="lens-wrapper">
              <img src="../assets/lens.svg" alt="放大镜" class="lens-icon" />
            </div>
             <!-- 视频拍摄区 -->
            <div class="video-section">
              <video controls class="video-player">
              <source src="../assets/output.mp4" type="video/mp4" />
                您的浏览器不支持视频播放。
              </video>
              <h2 class="video-title">战况拍摄</h2>
            </div>
          </div>
        </div>
        <div class="column right">
          <!-- ====== Player A 区 ====== -->
          <div class="box right-top">
            <!-- 第一行：标题 -->
            <div class="row row1">
              <h3 class="player-title">Player A 数据统计</h3>
            </div>
            <!-- 第二行：两张图表 -->
            <div class="row row2 charts">
              <div class="chart-container">
                <BarChart
                  :labels="strokeLabels(freqA)"
                  :data="strokeData(freqA)"
                />
              </div>
              <div class="chart-container">
                <PieChart
                  :labels="gradeLabels(freqA)"
                  :data="gradeData(freqA)"
                />
              </div>
            </div>
            <!-- 第三行：评价文字 -->
            <div class="row row3 eval-list">
              <div
                v-for="([label, count], idx) in evalItems(freqA)"
                :key="idx"
              >
                {{ label }} ({{ count }})
              </div>
            </div>
          </div>

          <!-- ====== Player B 区（同理） ====== -->
          <div class="box right-bottom">
            <div class="row row1">
              <h3 class="player-title">Player B 数据统计</h3>
            </div>
            <div class="row row2 charts">
              <div class="chart-container">
                <BarChart
                  :labels="strokeLabels(freqB)"
                  :data="strokeData(freqB)"
                />
              </div>
              <div class="chart-container">
                <PieChart
                  :labels="gradeLabels(freqB)"
                  :data="gradeData(freqB)"
                />
              </div>
            </div>
            <div class="row row3 eval-list">
              <div
                v-for="([label, count], idx) in evalItems(freqB)"
                :key="idx"
              >
                {{ label }} ({{ count }})
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import BarChart from '../components/BarChart.vue'
  import PieChart from '../components/PieChart.vue'

  export default {
    name: 'Analysis',
    components: { BarChart, PieChart },
    data() {
      return {
        freqA: [],
        freqB: []
      }
    },
    async mounted() {
      try {
        const [a, b] = await Promise.all([
          fetch('http://localhost:5000/api/player-a/freq').then(r=>r.json()),
          fetch('http://localhost:5000/api/player-b/freq').then(r=>r.json())
        ])
        this.freqA = a
        this.freqB = b
      } catch (e) {
        console.error(e)
      }
    },
    methods: {
      // 接球类型柱状图
      strokeLabels() { return ['正手','反手'] },
      strokeData(freq) {
        const map = Object.fromEntries(freq)
        return ['正手','反手'].map(k => map[k] || 0)
      },
      // 等级饼图
      gradeLabels() { return ['A','B','C'] },
      gradeData(freq) {
        const map = Object.fromEntries(freq)
        const total = ['A','B','C'].reduce((s,k)=>s + (map[k]||0),0)
        return ['A','B','C'].map(k =>
          total ? ((map[k]||0)/total*100).toFixed(1) : 0
        )
      },
      // 剩余的都是“评价类”文字
      evalItems(freq) {
        const skip = new Set(['正手','反手','A','B','C'])
        return freq.filter(([lab]) => !skip.has(lab))
      }
    }
  }
  </script>
  
  <style scoped>
    .analysis {
      flex-direction: column;
      text-align: center;
      min-height: 100vh;
      background-color: #FBFAFF;
    }
    
    /* 跟 Home.vue 一致的标题框样式 */
    .header-frame {
      width:100%;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #ffffff;
      border: 2px solid white;
      padding: 10px 20px;
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
    font-size: 48px;
    font-weight: bold;
    color: #281F7C;
    margin: 0;
  }

  .action-btn {
    position: absolute;
    right: 45px;
    background-color: #281F7C;
    border: 1px solid #281F7C;
    color: white;
    font-weight: bold;
    padding: 8px 16px;
    font-size: 14px;
    cursor: pointer;
    border-radius: 4px;
    bottom:24px;
  }

  /* 主体内容区 */
  .content-area {
    display: flex;
    gap: 20px;
    margin: 20px auto;
    /* 固定高度，可根据需求调整 */
    height:87vh;
    width:98%;
  }

  .column {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  /* 左右区：两个等高框 */
  .column.left{
    align-items: center;
    gap: 20px;
  }
  .column.center {
    align-items: center;
    justify-content: flex-start;
  }
  .column.right {
    align-items: center;
    gap: 10px;
  }
  .column.left .box{
    width:80%;
    height:50%;
  }
  .column.right .box {
    width:80%;
    height:50%;
  }

  /* 中区：单个大框 */
  .column.center .box {
  }

  /* 通用框样式 */
  .box {
    background: #ffffff;
    border: 2px solid #EBECFE;
    border-radius:20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: #281F7C;
  }

  /* 高度比 4:6 */
  .left-top { flex: 3.5; }
  .left-bottom { flex: 6.5; }

  .left-top {
    border-radius: 15px;
    width: 80%;
    background: #FFF5F3;
    border: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }

  /* 顶部天气部分 */
  .weather-top {
    width: 90%;
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: center;
  }

  .weather-icon {
    background-color: #FFF5F3;
    width: 150px;
    height: 150px;
    margin-right:30px;
  }

  .weather-info {
    display: flex;
    flex-direction: column;
    color: #FF7F27;
    font-size: 18px;
    font-weight: bold;
    align-items: flex-start;
  }

  .temperature,
  .condition {
    font-size:60px;
    line-height: 1.4;
  }

  /* 底部风速湿度部分 */
  .weather-bottom {
    width: 70%;
    display: flex;
    justify-content: space-between;
    color: #FF7F27;
    font-size: 48px;
    margin-top:50px;
  }

  .wind,
  .humidity {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;

  }

  .label{

    line-height: 1.4;
  }
  .value {
    font-size:36px;
    line-height: 1.4;
  }


  .left-bottom {
    background: #EBECFE;
    border: none;
  }

  /* 热力图框内部 */
  .heatmap-title {
    font-size: 32px;
    color: #281F7C;
    margin-bottom: 8px;
    font-weight: bold;
    writing-mode: vertical-rl;
    text-orientation: upright;
    margin-right:40px;
  }

  .heatmap-image {
    width: 74%;
    height: auto;
    object-fit: contain;
  }

  .center-box {
    position: relative;
    width: 90%;
    height: 80%;
    margin-top: 15vh;
    background: #99D9EA;
    border: none;
    z-index: 1;
  }

  /* 虚线圆环 */
  .center-box::before {
    content: '';
    position: absolute;
    top: -180px;
    left: 50%;
    transform: translateX(-50%);
    width: 120%;
    height: 90%;
    border-top: 5px dashed #99D9EA;
    border-left: 5px solid #99D9EA;
    border-right: 5px solid #99D9EA;
    border-bottom: none;
    border-radius: 70% 70% 70% 70%;
  }

 /* 放大镜及光圈 */
  .lens-wrapper {
    position: absolute;
    top: -40px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 80px;
    z-index: 2;
  }
  .lens-icon {
    position: relative;
    width: 100%;
    height: 100%;
    display: block;
  }
  /* 光圈 - 双环 */
  .lens-wrapper::before,
  .lens-wrapper::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    border: 2px solid #367E7F;
  }
  .lens-wrapper::before {
    width: 140px;
    height: 140px;
    opacity: 0.8;
    background-color: #507F80;
  }
  .lens-wrapper::after {
    width: 200px;
    height: 200px;
    opacity: 0.6;
    border-top: 5px dashed #367E7F;
    border-bottom: 5px dashed #367E7F;
  }

  /* 视频区 */
  .video-section {
    position: absolute;
    top: 110px;
    width: 90%;
    height: 90%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .video-title {
    font-size: 36px;
    color: #281F7C;
    font-weight: bold;
    z-index: 3;
    margin-top: 5px;
  }
  .video-player {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 20px;
  }
  .right-top {
    background: #EBECFE;
    border: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;    /* 改为顶对齐 */
    padding-top: 20px;               /* 控制顶部内边距 */
  }
  .right-bottom {
    background: #FFF5F3;
    border: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    justify-content: flex-start;    /* 改为顶对齐 */
    padding-top: 20px;               /* 控制顶部内边距 */
  }
  .player-title{
    margin: 0;
    display: flex;
    font-size: 36px;
    font-weight: bold;
    color: #281F7C;
    top: 0;
  }

  .freq-list {
    list-style: none;
    padding: 0;
    margin: 8px 0 0;
    text-align: left;
  }
  .freq-list li {
    margin-bottom: 4px;
    font-size: 14px;
    color: #281F7C;
  }

  /* 每一“行”都铺满宽度 */
  .row { 
    width: 95%; 
  }

  /* 第一行：标题水平居中 */
  .row1 {
    display: flex;
    justify-content: center;
    margin-bottom: 8px;
  }

  /* 图表行 */
  .charts {
    display: flex;
    gap: 16px;
    height: 200px;
    margin-bottom: 12px;
  }
  .chart-container {
    flex: 1;
    position: relative;
  }

  /* 文本评价行 */
  .eval-list {
    text-align: left;
    padding: 0 12px;
    overflow-y: auto;
    height:190px;
  }
  </style>
  
  