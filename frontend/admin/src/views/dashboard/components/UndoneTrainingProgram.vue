<template>
  <div class="container">
    <el-card class="table-card">
      <div slot="header">
        <span>未完成打分的培训项目</span>
      </div>
      <el-table v-loading="listLoading" :data="list" fit height="300" empty-text="暂无">
        <el-table-column prop="name" show-overflow-tooltip label="项目名称" />
        <el-table-column prop="endDate" show-overflow-tooltip label="结束时间" />
        <el-table-column prop="undoneCount" show-overflow-tooltip label="未评价人数" />
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { getUndoneTrainingProgramList } from '@/api/statistics'
export default {
  name: 'ContractEndInfo',
  data() {
    return {
      listLoading: false,
      list: []
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        this.listLoading = true,
        this.list = await getUndoneTrainingProgramList()
        console.log(this.list)
        this.listLoading = false
      } catch (error) {
        this.listLoading = false
        return
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.table-card{
    height: 400px;
}
</style>
