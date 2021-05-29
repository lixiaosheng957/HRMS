<template>
  <div class="app-container">
    <el-row class="header-row">
      <el-col :span="4">
        <el-page-header content="评价" @back="goBack" />
      </el-col>
    </el-row>
    <el-container>
      <el-main>
        <el-tabs v-model="activeName">
          <el-tab-pane label="未评价" name="first">
            <el-table v-loading="undoneListLoading" :data="undoneList" border fit>
              <el-table-column prop="id" label="编号" align="center" />
              <el-table-column prop="employeeName" label="姓名" align="center" />
              <el-table-column prop="employeeDepartment" label="部门" align="center" />
              <el-table-column label="操作" align="center">
                <template slot-scope="scope">
                  <el-button
                    type="primary"
                    size="mini"
                    round
                    @click="handleAssess(scope.row)"
                  >评价</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="已评价" name="second">
            <el-table v-loading="doneListLoading" :data="doneList" border fit>
              <el-table-column prop="id" label="编号" align="center" width="100" />
              <el-table-column prop="employeeName" label="姓名" align="center" />
              <el-table-column prop="employeeDepartment" label="部门" align="center" />
              <el-table-column prop="finishAssessTime" label="评价时间" align="center" />
              <el-table-column prop="level" label="评价等级" align="center" />
              <el-table-column label="操作" align="center">
                <template slot-scope="scope">
                  <el-button
                    type="primary"
                    size="mini"
                    round
                    @click="handleShowDetail(scope.row)"
                  >详情</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-main>
      <el-dialog title="评价" :visible.sync="assessDialog" :before-close="beforCloseAssessDialog">
        <el-form ref="assessForm" :model="assessForm" label-width="90px" :rules="rules">
          <el-form-item label="是否完成" prop="isFinish">
            <el-switch
              v-model="assessForm.isFinish"
              active-text="是"
              inactive-text="否"
              :active-value="true"
              :inactive-value="false"
            />
          </el-form-item>
          <el-form-item label="等级" class="align-center" prop="level">
            <el-rate
              v-model="assessForm.level"
              show-text
              :max="4"
              style="margin-top:10px;"
              :texts="['较差', '一般', '良好', '优秀']"
            />
          </el-form-item>
          <el-form-item label="评语" prop="assess">
            <el-input v-model="assessForm.assess" type="textarea" autosize maxlength="255" show-word-limit />
          </el-form-item>
          <el-row>
            <el-col :span="6" :offset="18">
              <el-button type="primary" @click="submitAssessForm('assessForm')">确定</el-button>
              <el-button @click="resetForm('assessForm')">重置</el-button>
            </el-col>
          </el-row>
        </el-form>
      </el-dialog>
      <el-dialog title="详情" :visible.sync="detalDialog">
        <el-form :model="assessDetail" label-width="90px" :rules="rules">
          <el-form-item label="是否完成" prop="isFinish">
            <el-switch
              v-model="assessDetail.isFinish"
              active-text="是"
              inactive-text="否"
              :active-value="true"
              :inactive-value="false"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="等级" class="align-center" prop="level">
            {{ assessDetail.level }}
          </el-form-item>
          <el-form-item label="评语" prop="assess">
            <el-input v-model="assessDetail.assess" :disabled="true" type="textarea" autosize maxlength="255" show-word-limit />
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
import {
  getUndoneAccessPeople,
  assess,
  getunFinishProgramDoneAssessList
} from '@/api/training'
import { Message } from 'element-ui'
export default {
  name: 'Assess',
  data() {
    return {
      undoneList: [],
      undoneListLoading: false,
      activeName: 'first',
      programName: '',
      assessDialog: false,
      assessForm: {
        isFinish: true,
        level: 1,
        assess: ''
      },
      rules: {
        isFinish: [{ required: true, message: '是否完成为必填', trigger: 'blur' }],
        level: [{ required: true, message: '必须指定等级', trigger: 'blur' }],
        assess: [{ required: true, message: '评语不能为空', trigger: 'blur' }]
      },
      currentAssessId: null,
      doneList: [],
      doneListLoading: false,
      assessDetail: {
        assess: '',
        isFinish: null,
        level: ''
      },
      detalDialog: false
    }
  },
  watch: {
    activeName: function(val) {
      if (val === 'first') {
        this.getUndoneList({ id: this.$route.params.id })
      } else {
        this.getDoneList({ id: this.$route.params.id })
      }
    }
  },
  created() {
    this.getUndoneList({ id: this.$route.params.id })
  },
  methods: {
    goBack() {
      this.$router.back(-1)
    },
    async getUndoneList(params = null) {
      try {
        this.undoneListLoading = true
        this.undoneList = await getUndoneAccessPeople(params)
        this.undoneListLoading = false
      } catch (error) {
        this.undoneListLoading = false
        return
      }
    },
    async getDoneList(params = null) {
      try {
        this.doneListLoading = true
        this.doneList = await getunFinishProgramDoneAssessList(params)
        this.doneListLoading = false
      } catch (error) {
        this.doneListLoading = false
        return
      }
    },
    handleAssess({ id }) {
      this.assessDialog = true
      this.currentAssessId = id
    },
    rate2String(rate) {
      let str = ''
      switch (rate) {
        case 1:
          str = '较差'
          break
        case 2:
          str = '一般'
          break
        case 3:
          str = '良好'
          break
        case 4:
          str = '优秀'
          break
        default:
          str = ''
          break
      }
      return str
    },
    submitAssessForm(formName) {
      this.$refs[formName].validate(async(valid) => {
        if (valid) {
          try {
            const submitObj = { ...this.assessForm }
            submitObj.id = this.currentAssessId
            submitObj.level = this.rate2String(submitObj.level)
            await assess(submitObj)
            Message({
              message: '评价成功',
              type: 'success',
              duration: 2000
            })
            this.resetForm(formName)
            this.currentAssessId = null
            this.assessDialog = false
            this.getUndoneList({ id: this.$route.params.id })
          } catch (error) {
            return
          }
        } else {
          return
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    beforCloseAssessDialog(done) {
      this.$confirm('确认关闭？关闭后会失去保存的数据', '提示')
        .then((_) => {
          done()
          this.resetForm('assessForm')
          this.currentAssessId = null
        })
        .catch((_) => {})
    },
    handleShowDetail(row) {
      this.detalDialog = true
      Object.keys(this.assessDetail).forEach(key => {
        this.assessDetail[key] = row[key]
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.header-row{
    padding:0 20px;
    display: flex;
    align-items: center;
}
// .align-center{
//     display: flex;
//     align-items: center;
// }
</style>
