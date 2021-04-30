<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="3">
            <h3>培训打分</h3>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-tabs v-model="activeName">
          <el-tab-pane label="未完成" name="first">
            <el-table v-loading="UndoneAssessProgramListLoading" :data="UndoneAssessProgramList" border fit height="500">
              <el-table-column prop="id" label="编号" width="100" align="center" />
              <el-table-column prop="name" label="项目名称" show-overflow-tooltip width="200" align="center" />
              <el-table-column prop="address" label="培训地址" show-overflow-tooltip width="200" align="center" />
              <el-table-column prop="beginDate" label="培训开始时间" width="150" align="center" />
              <el-table-column prop="endDate" label="培训结束时间" width="150" align="center" />
              <el-table-column prop="undoneAssessCount" label="未评分人数" width="150" align="center" />
              <el-table-column label="操作" align="center">
                <template slot-scope="scope">
                  <el-button
                    type="primary"
                    size="mini"
                    round
                    @click="handleGoToAssess(scope.row)"
                  >去打分</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="已完成" name="second">
            <el-table v-loading="doneAssessProgramListLoading" :data="doneAssessProgramList" border fit height="500">
              <el-table-column prop="id" label="编号" width="100" align="center" />
              <el-table-column prop="name" label="项目名称" show-overflow-tooltip width="200" align="center" />
              <el-table-column prop="address" label="培训地址" show-overflow-tooltip width="200" align="center" />
              <el-table-column prop="beginDate" label="培训开始时间" width="150" align="center" />
              <el-table-column prop="endDate" label="培训结束时间" width="150" align="center" />
              <el-table-column label="操作" align="center">
                <template slot-scope="scope">
                  <el-button
                    type="primary"
                    size="mini"
                    round
                    @click="handleShowDoneDetail(scope.row)"
                  >详情</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-main>
      <el-dialog title="详情" :visible.sync="detailDialog">
        <el-tabs v-model="detailActiveTabs">
          <el-tab-pane label="项目信息" name="first">
            <el-form ref="form" :model="detail" label-width="80px">
              <el-form-item label="项目名称">
                <el-input
                  v-model="detail.name"
                  type="text"
                  :disabled="true"
                />
              </el-form-item>
              <el-form-item label="具体内容">
                <el-input
                  v-model="detail.content"
                  type="textarea"
                  :disabled="true"
                />
              </el-form-item>
              <el-form-item label="培训地址">
                <el-input
                  v-model="detail.address"
                  type="text"
                  :disabled="true"
                />
              </el-form-item>
              <el-form-item label="开始时间">
                <el-input
                  v-model="detail.beginDate"
                  type="text"
                  :disabled="true"
                />
              </el-form-item>
              <el-form-item label="结束时间">
                <el-input
                  v-model="detail.endDate"
                  type="text"
                  :disabled="true"
                />
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="评价记录" name="second">
            <el-table :data="detail.records" height="300">
              <el-table-column prop="id" label="编号" width="80px" align="center" />
              <el-table-column prop="employeeName" label="姓名" align="center" />
              <el-table-column prop="departmentName" show-overflow-tooltip label="部门" align="center" />
              <el-table-column prop="finishAssessTime" show-overflow-tooltip label="评价时间" align="center" />
              <el-table-column label="操作" align="center">
                <template slot-scope="scope">
                  <el-button
                    type="primary"
                    size="mini"
                    round
                    @click="handleShowAssessDetail(scope.row)"
                  >
                    详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-dialog>
      <el-dialog title="评价详情" :visible.sync="assessDetailDialog">
        <el-form :model="assessDetail" label-width="90px">
          <el-form-item label="是否完成">
            <el-switch
              v-model="assessDetail.isFinish"
              active-text="是"
              inactive-text="否"
              :active-value="true"
              :inactive-value="false"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="等级" class="align-center">
            {{ assessDetail.level }}
          </el-form-item>
          <el-form-item label="评语">
            <el-input v-model="assessDetail.assess" :disabled="true" type="textarea" autosize maxlength="255" show-word-limit />
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
import {
  getUnfinishAssessProgramList,
  getFinishAssProgramList,
  getFinishAssProgramDetail
} from '@/api/training'
export default {
  name: 'ProgramAssess',
  data() {
    return {
      activeName: 'first',
      UndoneAssessProgramList: [],
      UndoneAssessProgramListLoading: false,
      doneAssessProgramList: [],
      doneAssessProgramListLoading: false,
      detailDialog: false,
      detailActiveTabs: 'first',
      detail: {
        name: '',
        content:
          '',
        address: '',
        beginDate: '',
        endDate: '',
        records: []
      },
      assessDetailDialog: false,
      assessDetail: {
        assess: '',
        level: '',
        isFinish: null
      }
    }
  },
  watch: {
    activeName: function(val) {
      if (val === 'first') {
        this.getUndoneAssessProgramList()
      } else {
        this.getDoneAssessProgramList()
      }
    }
  },
  created() {
    this.getUndoneAssessProgramList()
  },
  methods: {
    async getUndoneAssessProgramList(params = null) {
      try {
        this.UndoneAssessProgramListLoading = true
        this.UndoneAssessProgramList = await getUnfinishAssessProgramList(params)
        this.UndoneAssessProgramListLoading = false
      } catch (error) {
        this.UndoneAssessProgramListLoading = false
        return
      }
    },
    handleGoToAssess({ id }) {
      this.$router.push({
        path: `/training/assess/${id}`
      })
    },
    async getDoneAssessProgramList(params = null) {
      try {
        this.doneAssessProgramListLoading = true
        this.doneAssessProgramList = await getFinishAssProgramList(params)
        this.doneAssessProgramListLoading = false
      } catch (error) {
        this.doneAssessProgramListLoading = false
        return
      }
    },
    async handleShowDoneDetail({ id }) {
      this.detailDialog = true
      try {
        this.detail = await getFinishAssProgramDetail({ id })
      } catch (error) {
        this.detailDialog = false
        return
      }
    },
    handleShowAssessDetail(row) {
      this.assessDetailDialog = true
      Object.keys(this.assessDetail).forEach(key => {
        this.assessDetail[key] = row[key]
      })
    }
  }
}
</script>

<style>

</style>
