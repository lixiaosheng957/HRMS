<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="3">
            <h3>离职员工</h3>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-table v-loading="moveListLoading" :data="employeeMoveList" border height="560" width="100%" fit element-loading-text="加载中">
          <el-table-column prop="id" label="员工编号" align="center" width="80" />
          <el-table-column prop="name" label="员工姓名" align="center" width="150" />
          <el-table-column prop="gender" label="性别" align="center" width="80" />
          <el-table-column prop="phone" label="电话" align="center" width="200" />
          <el-table-column prop="department" label="部门" align="center" width="200" />
          <el-table-column prop="job" label="职位" align="center" width="200" />
          <el-table-column prop="type" label="员工类型" align="center" width="200" />
          <el-table-column label="操作" align="center" fixed="right">
            <template slot-scope="scope">
              <el-button type="primary" size="mini" round @click="getMoveDetail(scope.row)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
      <el-dialog title="详情" :visible.sync="showDetailDialog">
        <el-form ref="employeeMoveForm" :model="detail" label-width="90px">
          <el-form-item label="离职原因">
            <el-input v-model="detail.reason" :disabled="true" type="textarea" placeholder="请输入离职原因" />
          </el-form-item>
          <el-form-item label="离职时间">
            <el-date-picker v-model="detail.moveTime" :disabled="true" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
import { getEmployeeMoveDetail, getEmployeeMoveList } from '@/api/employee'
export default {
  name: 'EmployeeMove',
  data() {
    return {
      moveListLoading: false,
      employeeMoveList: [],
      showDetailDialog: false,
      detail: {
        reason: '',
        moveTime: ''
      }
    }
  },
  created() {
    this.fetchEmployeeMoveList()
  },
  methods: {
    async fetchEmployeeMoveList(params = null) {
      try {
        this.moveListLoading = true
        this.employeeMoveList = await getEmployeeMoveList(params)
        this.moveListLoading = false
      } catch (error) {
        this.moveListLoading = false
      }
    },
    async getMoveDetail({ id }) {
      try {
        this.showDetailDialog = true
        const res = await getEmployeeMoveDetail({ id })
        Object.keys(this.detail).forEach(key => {
          this.detail[key] = res[key]
        })
      } catch (error) {
        this.showDetailDialog = false
        return
      }
    }
  }
}
</script>

<style>

</style>
