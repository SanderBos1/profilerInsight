<template>
  <div>
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';

// Register the components you need from Chart.js
ChartJS.register(Title, Tooltip, Legend, ArcElement);

export default {
  name: 'basePieChart',
  props:{
    values: Array,
    labels: Array,
    backgroundColor: Array
  },
  components: {
    Pie
  },
  data() {
    return {
      chartData: {  
        labels: this.labels,
        datasets: [
          {
            label: 'My Pie Chart',
            backgroundColor: this.backgroundColor,
            data: this.values
          }
        ]
      },
      chartOptions: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                let label = context.label || '';
                if (context.parsed) {
                  label += `: ${context.parsed}`;
                }
                return label;
              }
            }
          }
        }
      }
    };
  }
};
</script>

<style scoped>
/* Add any styles you need here */
</style>