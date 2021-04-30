<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="3">
            <h3>操作记录</h3>
          </el-col>
          <el-col :span="3">
            <el-input v-model="query.type" type="text" clearable placeholder="根据操作类型查找" />
          </el-col>
          <el-col :span="8" style="margin-left:10px;">
            <el-date-picker
              v-model="query.timeRange"
              type="datetimerange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="yyyy-MM-dd HH:mm:ss"
            />
          </el-col>
          <el-col :span="2">
            <el-button type="primary" icon="el-icon-search" @click="handleQuery">查询</el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-table v-loading="listLoading" :data="list">
          <el-table-column prop="id" label="编号" align="center" />
          <el-table-column prop="type" label="操作类型" show-overflow-tooltip align="center" />
          <el-table-column prop="content" label="操作内容" show-overflow-tooltip align="center" />
          <el-table-column prop="time" label="操作时间" align="center" />
        </el-table>
        <el-row class="pagination">
          <el-col :span="24" class="pagination-content">
            <el-pagination
              :current-page="currentPage"
              :page-sizes="[10, 20, 30, 40]"
              :page-size="pageSize"
              layout="total, sizes, prev, pager, next"
              :total="total"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { getMyOperateLog } from '@/api/operateLog'
export default {
  name: 'OperateLogView',
  data() {
    return {
      list: [],
      listLoading: false,
      currentPage: 1,
      pageSize: 10,
      total: 0,
      query: {
        type: '',
        timeRange: []
      }
    }
  },
  created() {
    this.getMyOperateLogList({ page: 1, pageSize: 10 })
  },
  methods: {
    async getMyOperateLogList(params = null) {
      try {
        this.listLoading = true
        const res = await getMyOperateLog(params)
        this.list = res.data
        this.total = res.total
        this.listLoading = false
      } catch (error) {
        this.listLoading = false
        return
      }
    },
    handleQuery() {
      if (!this.checkQuery()) {
        this.getMyOperateLogList({ page: 1, pageSize: this.pageSize })
      } else {
        this.getMyOperateLogList({
          page: 1,
          pageSize: this.pageSize,
          type: this.query.type ? this.query.type : undefined,
          startTime: this.query.timeRange.length === 2 ? this.query.timeRange[0] : undefined,
          endTime: this.query.timeRange.length === 2 ? this.query.timeRange[1] : undefined
        })
      }
    },
    checkQuery() {
      if (!this.query.type && (this.query.timeRange === null || this.query.timeRange.length === 0)) {
        return false
      }
      return true
    },
    handleSizeChange(val) {
      this.pageSize = val
      if (!this.checkQuery()) {
        this.getMyOperateLogList({
          page: this.currentPage,
          pageSize: this.pageSize
        })
      } else {
        this.getMyOperateLogList({
          page: this.currentPage,
          pageSize: this.pageSize,
          ...this.query
        })
      }
    },
    handleCurrentChange(val) {
      this.currentPage = val
      if (!this.checkQuery()) {
        this.getMyOperateLogList({
          page: this.currentPage,
          pageSize: this.pageSize
        })
      } else {
        this.getMyOperateLogList({
          page: this.currentPage,
          pageSize: this.pageSize,
          ...this.query
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.pagination{
    margin-top: 20px;
}
.pagination-content{
    display: flex;
    justify-content: center;
}
</style>
