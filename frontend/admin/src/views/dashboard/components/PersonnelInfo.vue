<template>
  <div class="container">
    <el-card class="item">
      <div class="content">
        <span>本月入职：</span>
        <span>{{ data.join }}</span>
        <span> 人</span>
      </div>
    </el-card>
    <el-card class="item box-card">
      <div class="content">
        <span>本月变动：</span>
        <span>{{ data.transfer }}</span>
        <span> 人</span>
      </div>
    </el-card>
    <el-card class="item">
      <div class="content">
        <span>本月续约：</span>
        <span>{{ data.renew }}</span>
        <span> 人</span>
      </div>
    </el-card>
    <el-card class="item">
      <div class="content">
        <span>本月离职：</span>
        <span>{{ data.move }}</span>
        <span> 人</span>
      </div>
    </el-card>
  </div>
</template>

<script>
import { statisticsPersonnelInfo } from '@/api/statistics'
export default {
  name: 'PersonnelStatistics',
  data() {
    return {
      data: {
        join: 0,
        move: 0,
        renew: 0,
        transfer: 0
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const res = await statisticsPersonnelInfo()
        Object.keys(this.data).forEach(key => {
          this.data[key] = res[key]
        })
      } catch (error) {
        return
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.container{
    height: 400px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    .item{
        height: 80px;
        font-size: 20px;
        font-weight: bold;
        display: flex;
        align-items: center;
    }
}
</style>
