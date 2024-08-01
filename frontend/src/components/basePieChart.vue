<template>
  <div class="chart-container">
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';

// Register the necessary components from Chart.js
ChartJS.register(Title, Tooltip, Legend, ArcElement);

export default {
  name: 'BasePieChart',
  props: {
    values: {
      type: Array,
      default: () => []
    },
    labels: {
      type: Array,
      default: () => []
    },
    backgroundColor: {
      type: Array,
      default: () => []
    }
  },
  components: {
    Pie
  },
  computed: {
    chartData() {
      return {
        labels: this.labels,
        datasets: [
          {
            label: 'My Pie Chart',
            backgroundColor: this.backgroundColor,
            data: this.values
          }
        ]
      };
    },
    chartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                let label = context.label || '';
                if (context.parsed) {
                  label += `: ${context.parsed}`;
                }
                return label;
              }
            }
          }
        }
      };
    }
  }
};
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  max-width: 500px; /* Set your desired maximum width here */
  height: auto; /* Let the height adjust based on width */
  margin: 0 auto; /* Center the chart horizontally */
}
</style>
