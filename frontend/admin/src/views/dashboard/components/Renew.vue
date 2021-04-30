<template>
  <div class="container">
    <el-card class="table-card">
      <div slot="header">
        <span>合同即将到期待续约</span>
      </div>
      <el-table v-loading="listLoading" :data="list" fit height="300" empty-text="暂时没有合同快到期的员工">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="departmentName" show-overflow-tooltip label="所属部门" />
        <el-table-column prop="contractEndDate" show-overflow-tooltip label="合同结束时间" />
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { getToBeRenewList } from '@/api/statistics'
export default {
  name: 'RenewInfo',
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
        this.list = await getToBeRenewList()
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
