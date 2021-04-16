<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="3">
            <h3>变动记录</h3>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-table v-loading="listLoading" :data="recordsList" border fit width="100%" element-loading-text="加载中">
          <el-table-column label="编号" prop="id" />
        </el-table>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { getTransferRecordsList } from '@/api/employee'
export default {
  name: 'TransferRecord',
  data() {
    return {
      listLoading: false,
      recordsList: []
    }
  },
  methods: {
    async fetchData() {
      try {
        this.listLoading = true
        this.recordsList = await getTransferRecordsList()
        this.listLoading = false
      } catch (error) {
        this.listLoading = false
      }
    }
  }
}
</script>

<style>

</style>
