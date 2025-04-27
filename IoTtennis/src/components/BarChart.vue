<template>
  <canvas ref="canvas" />
</template>

<script>
import { defineComponent, ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

export default defineComponent({
  name: 'BarChart',
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
        type: 'bar',
        data: {
          labels: props.labels,
          datasets: [{
            label: '次数',
            data: props.data,
            backgroundColor: 'rgba(39,125,191,0.5)'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { title: { display: true, text: '接球类型' } },
            y: { title: { display: true, text: '次数' } }
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


  