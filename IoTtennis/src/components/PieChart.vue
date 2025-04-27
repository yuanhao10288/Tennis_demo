<template>
    <canvas ref="canvas" />
  </template>
  
  <script>
  import { defineComponent, ref, onMounted, watch } from 'vue'
  import Chart from 'chart.js/auto'
  
  export default defineComponent({
    name: 'PieChart',
    props: {
      labels: { type: Array, required: true },
      data:   { type: Array, required: true }
    },
    setup(props) {
      const canvas = ref(null)
      let chart
  
      const renderChart = () => {
        if (chart) chart.destroy()
        chart = new Chart(canvas.value, {
          type: 'pie',
          data: {
            labels: props.labels,
            datasets: [{
              data: props.data,
              backgroundColor: ['#FF6384','#36A2EB','#FFCE56']
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { position: 'bottom' },
              tooltip: { callbacks: {
                label: ctx => `${ctx.label}: ${ctx.parsed}%`
              }}
            }
          }
        })
      }
  
      onMounted(renderChart)
      watch([() => props.labels, () => props.data], renderChart)
  
      return { canvas }
    }
  })
  </script>
  
  <style scoped>
  canvas { width: 100%; height: 100%; }
  </style>
  
  