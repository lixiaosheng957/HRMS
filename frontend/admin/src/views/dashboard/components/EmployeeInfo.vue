<template>
  <div style="height:400px;width:100%;" />
</template>

<script>
import * as echarts from 'echarts'
import { statisticsForDepartmentEmployeeCount } from '@/api/statistics'
export default {
  name: 'EmployeeTotal',
  data() {
    return {
      chart: null,
      data: null
    }
  },
  async mounted() {
    try {
      this.data = await statisticsForDepartmentEmployeeCount()
    } catch (error) {
      console.log(error)
    }
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el)
      this.chart.setOption({
        title: {
          text: '员工分布图',
          left: '仅统计在职的员工'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['正式员工', '试用员工', '实习员工']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 20]
        },
        yAxis: {
          type: 'category',
          data: this.data.departmentNameArray
        },
        series: [
          {
            name: '正式员工',
            type: 'bar',
            data: this.data.fullTimeEmployees
          },
          {
            name: '试用员工',
            type: 'bar',
            data: this.data.probationPeriodEmployees
          },
          {
            name: '实习员工',
            type: 'bar',
            data: this.data.internshipEmployees
          }
        ]
      })
    }
  }
}
</script>

<style>

</style>
