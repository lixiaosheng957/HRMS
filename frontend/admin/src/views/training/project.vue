<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row class="header">
          <el-col :span="3">
            <h3>培训项目管理</h3>
          </el-col>
          <el-col :span="4">
            <el-input
              v-model="searchinput"
              type="text"
              placeholder="请输入项目名称"
            />
          </el-col>
          <el-col :span="1">
            <el-button
              style="margin-left:5px;"
              type="primary"
              icon="el-icon-search"
              @click="handleSearch"
            >搜索</el-button>
          </el-col>
          <el-col :span="2" :offset="11">
            <el-button
              type="primary"
              style="float: right"
              @click="showAddTrainingProgram"
            >增加培训项目</el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-table
          v-loading="listLoading"
          :data="trainList"
          width="100%"
          border
          fit
          max-height="500"
        >
          >
          <el-table-column prop="id" label="项目编号" width="100" align="center" />
          <el-table-column prop="name" label="项目名称" show-overflow-tooltip width="200" align="center" />
          <el-table-column prop="address" label="培训地址" show-overflow-tooltip width="200" align="center" />
          <el-table-column prop="beginDate" label="培训开始时间" width="150" align="center" />
          <el-table-column prop="endDate" label="培训结束时间" width="150" align="center" />
          <el-table-column prop="step" label="状态" width="150" align="center" />
          <el-table-column label="操作" align="center">
            <template slot-scope="scope">
              <el-button
                slot="reference"
                style="margin-right:10px;"
                type="primary"
                size="mini"
                round
                :disabled="scope.row.isPublish"
                @click="handlePublish(scope.row)"
              >
                发布
              </el-button>
              <el-button
                type="primary"
                size="mini"
                round
                @click.native.prevent="showDetail(scope.row)"
              >
                查看
              </el-button>
              <el-button
                type="primary"
                size="mini"
                round
                :disabled="scope.row.isPublish"
                @click.native.prevent="handleShowEditProgramDialog(scope.row)"
              >编辑</el-button>
              <el-button
                type="danger"
                size="mini"
                round
                @click.native.prevent="handleDeleteProgram(scope.row)"
              >
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
    <el-dialog
      title="增加培训项目"
      :visible.sync="addDialogVisible"
      width="50%"
      :before-close="handleCloseAddTrainingProgramDialog"
    >
      <el-steps :active="addTrainingProgramStep" align-center style="margin-bottom:10px;">
        <el-step title="填写项目相关信息" />
        <el-step title="添加参与人员" />
      </el-steps>
      <el-form v-show="addTrainingProgramStep===1" ref="addform" :model="addProgramBaseForm" :rules="rules" label-width="80px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="addProgramBaseForm.name" type="text" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="具体内容" prop="content">
          <el-input v-model="addProgramBaseForm.content" type="textarea" placeholder="请输入具体内容" />
        </el-form-item>
        <el-form-item label="培训地址" prop="address">
          <el-input v-model="addProgramBaseForm.address" type="textarea" placeholder="请输入培训地址" />
        </el-form-item>
        <el-form-item label="开始时间" prop="beginDate">
          <el-date-picker
            v-model="addProgramBaseForm.beginDate"
            type="date"
            placeholder="选择日期"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="endDate">
          <el-date-picker
            v-model="addProgramBaseForm.endDate"
            type="date"
            placeholder="选择日期"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
      </el-form>
      <div v-show="addTrainingProgramStep===2" class="transfer-container">
        <el-transfer
          v-model="selectedEmployeeList"
          filterable
          :filter-method="filterEmployeeMethod"
          filter-placeholder="请输入拼音查找"
          :data="employeeList"
          :titles="['员工名单','参加名单']"
        />
      </div>
      <el-row style="margin-top:15px;">
        <el-col :span="6" :offset="18">
          <el-button type="primary" @click="handleAddTrainingProgram('addform','primaryButton')">{{ addTrainingProgramStep===1?"下一步":"确定" }}</el-button>
          <el-button @click="handleAddTrainingProgram('addform','minorButton')">{{ addTrainingProgramStep===1?"重置":"上一步" }}</el-button>
        </el-col>
      </el-row>
    </el-dialog>
    <el-dialog
      title="查看详情"
      :visible.sync="showDetailDialogVisible"
      width="50%"
    >
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
        <el-tab-pane label="参与人信息" name="second">
          <el-table :data="detail.participant" height="300">
            <el-table-column prop="id" label="编号" width="80px" align="center" />
            <el-table-column prop="name" label="姓名" width="120" align="center" />
            <el-table-column prop="type" label="类型" width="120" align="center" />
            <el-table-column prop="departmentName" show-overflow-tooltip label="部门" width="120" align="center" />
            <el-table-column prop="phone" label="手机号" width="130" align="center" />
            <el-table-column prop="email" label="邮箱" show-overflow-tooltip width="150px" align="center" />
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
    <el-dialog title="编辑项目" :visible.sync="showEditProgramDialog" :before-close="handleBeforCloseEditDialog">
      <el-tabs v-model="editTypeActive">
        <el-tab-pane label="基础信息" name="first">
          <el-form ref="editform" :model="editProgramBaseForm" :rules="rules" label-width="80px">
            <el-form-item label="项目名称" prop="name">
              <el-input v-model="editProgramBaseForm.name" type="text" placeholder="请输入项目名称" />
            </el-form-item>
            <el-form-item label="具体内容" prop="content">
              <el-input v-model="editProgramBaseForm.content" type="textarea" placeholder="请输入具体内容" />
            </el-form-item>
            <el-form-item label="培训地址" prop="address">
              <el-input v-model="editProgramBaseForm.address" type="textarea" placeholder="请输入培训地址" />
            </el-form-item>
            <el-form-item label="开始时间" prop="beginDate">
              <el-date-picker
                v-model="editProgramBaseForm.beginDate"
                type="date"
                placeholder="选择日期"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>
            <el-form-item label="结束时间" prop="endDate">
              <el-date-picker
                v-model="editProgramBaseForm.endDate"
                type="date"
                placeholder="选择日期"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="参与人员" name="second">
          <div class="transfer-container">
            <el-transfer
              v-model="participantList"
              filterable
              :filter-method="filterEmployeeMethod"
              filter-placeholder="请输入拼音查找"
              :data="employeeList"
              :titles="['员工名单','参加名单']"
            />
          </div>
        </el-tab-pane>
        <el-row>
          <el-col :span="6" :offset="18">
            <el-button type="primary" @click="handleSubmitEdit">确定</el-button>
            <el-button @click="handleBeforCloseEditDialog">取消</el-button>
          </el-col>
        </el-row>
      </el-tabs>
    </el-dialog>
  </div>
</template>
<script>
import {
  addTrainingProgram,
  deleteTrainingProgram,
  getTrainingProgramList,
  getTrainingProgramDetail,
  publishProgram,
  editProgramBaseInfo,
  editProgramParticipant
} from '@/api/training'
import { getEmployeeList } from '@/api/employee'
import { Message } from 'element-ui'
export default {
  name: '',
  data() {
    return {
      // 搜索栏
      searchinput: '',
      addProgramBaseForm: {
        name: '',
        content: '',
        address: '',
        beginDate: null,
        endDate: null
      },
      rules: {
        name: [{ required: true, message: '项目名称不能为空', trigger: 'blur' }],
        content: [{ required: true, message: '培训内容不能为空', trigger: 'blur' }],
        address: [{ required: true, message: '培训地址不能为空', trigger: 'blur' }],
        beginDate: [{ required: true, message: '培训开始时间不能为空', trigger: 'blur' }],
        endDate: [{ required: true, message: '培训结束时间不能为空', trigger: 'blur' }]
      },
      listLoading: false,
      addDialogVisible: false,
      addTrainingProgramStep: 1,
      employeeList: [],
      selectedEmployeeList: [],
      showId: '',
      deleteId: '',
      showDetailDialogVisible: false,
      detail: {
        name: '',
        content:
          '',
        address: '',
        beginDate: '',
        endDate: '',
        participant: []
      },
      detailActiveTabs: 'first',
      trainList: [],
      showEditProgramDialog: false,
      participantList: [],
      editTypeActive: 'first',
      editProgramBaseForm: {
        programId: null,
        name: '',
        content: '',
        address: '',
        beginDate: '',
        endDate: ''
      },
      currentEditId: null
    }
  },
  watch: {
    editTypeActive: async function(val) {
      if (this.showEditProgramDialog) {
        if (val === 'first') {
          const res = await getTrainingProgramDetail({ id: this.currentEditId })
          Object.keys(this.editProgramBaseForm).forEach(key => {
            this.editProgramBaseForm[key] = res[key]
          })
        } else {
          const res = await getEmployeeList({ tags: true })
          const temp = []
          res.forEach((item) => {
            temp.push({
              label: item.label,
              key: item.value
            })
          })
          this.employeeList = temp
          this.participantList = await getTrainingProgramDetail({ id: this.currentEditId, justParticipant: true })
        }
      }
    }
  },
  mounted() {
    this.getTrainingProgramList()
  },
  methods: {
    // 增
    async showAddTrainingProgram() {
      this.addDialogVisible = true
      console.log(this.$refs)
      try {
        const res = await getEmployeeList({ tags: true })
        const temp = []
        res.forEach((item) => {
          temp.push({
            label: item.label,
            key: item.value
          })
        })
        this.employeeList = temp
      } catch (error) {
        return
      }
    },
    filterEmployeeMethod(query, item) {
      return item.label.indexOf(query) > -1
    },
    async handleAddTrainingProgram(formName, button) {
      if (this.addTrainingProgramStep === 1) {
        if (button === 'primaryButton') {
          this.$refs[formName].validate((valid) => {
            if (valid) {
              this.addTrainingProgramStep = 2
            } else {
              Message({
                message: '请按规则填完表单',
                type: 'warning',
                duration: '2000'
              })
            }
          })
        } else {
          this.resetForm(formName)
        }
      } else {
        if (button === 'primaryButton') {
          try {
            console.log(this.selectedEmployeeList)
            const submitObj = { ...this.addProgramBaseForm }
            submitObj.trainingPeople = this.selectedEmployeeList
            await this.$confirm('是否在创建后立即发布?', '确认信息', {
              distinguishCancelAndClose: true,
              confirmButtonText: '是',
              cancelButtonText: '否'
            })
            if (this.selectedEmployeeList.length === 0) {
              throw new Error('notSelected')
            }
            submitObj.isPublish = true
            await addTrainingProgram(submitObj)
            Message({
              message: '添加成功',
              type: 'success',
              duration: 2000
            })
            this.resetForm(formName)
            this.addTrainingProgramStep = 1
            this.selectedEmployeeList = []
            this.addDialogVisible = false
            this.getTrainingProgramList()
          } catch (error) {
            if (typeof error === 'string') {
              if (error === 'cancel') {
                const submitObj = { ...this.addProgramBaseForm }
                submitObj.trainingPeople = this.selectedEmployeeList
                submitObj.isPublish = false
                await addTrainingProgram(submitObj)
                Message({
                  message: '添加成功',
                  type: 'success',
                  duration: 2000
                })
                this.resetForm(formName)
                this.addTrainingProgramStep = 1
                this.selectedEmployeeList = []
                this.addDialogVisible = false
                this.getTrainingProgramList()
              } else if (error === 'colse') {
                return
              } else {
                Message({
                  message: '没有选择参与人员，不能发布',
                  type: 'warning',
                  duration: 2000
                })
                return
              }
            }
          }
        } else {
          this.addTrainingProgramStep = 1
        }
      }
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    handleCloseAddTrainingProgramDialog(done) {
      this.$confirm('确认关闭？关闭后会失去保存的数据', '提示')
        .then((_) => {
          done()
          this.resetForm('addForm')
          this.addTrainingProgramStep = 1
          this.selectedEmployeeList = []
        })
        .catch((_) => {})
    },
    handleDeleteProgram({ id }) {
      this.$confirm('确认删除吗？删除后会参与人员的记录也会删除', '提示')
        .then(async(_) => {
          try {
            await deleteTrainingProgram({ id })
            Message({
              message: '删除成功',
              type: 'success',
              duration: 2000
            })
            this.getTrainingProgramList()
          } catch (error) {
            return
          }
        })
        .catch((_) => {})
    },
    deleteTrainingProgram(val) {
      deleteTrainingProgram(val).then((response) => {
        if (response.data) {
          this.getTrainingProgramList()
        }
      })
    },
    async showDetail({ id }) {
      this.showDetailDialogVisible = true
      try {
        this.detail = await getTrainingProgramDetail({ id: id })
      } catch (error) {
        this.showDetailDialogVisible = false
      }
    },
    async getTrainingProgramList(params = null) {
      try {
        this.listLoading = true
        this.trainList = await getTrainingProgramList(params)
        this.listLoading = false
      } catch (error) {
        this.listLoading = false
        console.log(error)
      }
    },
    handleSearch() {
      this.getTrainingProgramList({ name: this.searchinput })
    },
    async handlePublish({ id }) {
      this.$confirm('确认发布吗？', '提示')
        .then(async(_) => {
          try {
            await publishProgram({ id })
            Message({
              message: '发布成功',
              type: 'success',
              duration: 2000
            })
            this.getTrainingProgramList()
          } catch (error) {
            return
          }
        })
        .catch((_) => {})
    },
    async handleShowEditProgramDialog({ id }) {
      console.log(this.editTypeActive)
      try {
        this.showEditProgramDialog = true
        if (this.editTypeActive === 'first') {
          const res = await getTrainingProgramDetail({ id })
          Object.keys(this.editProgramBaseForm).forEach(key => {
            this.editProgramBaseForm[key] = res[key]
          })
          this.currentEditId = id
        } else {
          const res = await getEmployeeList({ tags: true })
          const temp = []
          res.forEach((item) => {
            temp.push({
              label: item.label,
              key: item.value
            })
          })
          this.employeeList = temp
          this.participantList = await getTrainingProgramDetail({ id, justParticipant: true })
          this.currentEditId = id
        }
      } catch (error) {
        this.showEditProgramDialog = false
        return
      }
    },
    async handleSubmitEdit() {
      try {
        if (this.editTypeActive === 'first') {
          const formName = 'editform'
          this.$refs[formName].validate(async(valid) => {
            if (valid) {
              const submitObj = { ...this.editProgramBaseForm }
              submitObj.programId = this.currentEditId
              try {
                await editProgramBaseInfo(submitObj)
                Message({
                  message: '修改成功',
                  type: 'success',
                  duration: 2000
                })
                this.resetForm('editform')
                this.currentEditId = null
                this.editTypeActive = 'first'
                this.showEditProgramDialog = false
                this.getTrainingProgramList()
              } catch (error) {
                return
              }
            } else {
              Message({
                message: '请先按规则填完表单',
                type: 'warning',
                duration: 2000
              })
              return
            }
          })
        } else {
          await editProgramParticipant({
            id: this.currentEditId,
            trainingPeople: this.participantList
          })
          Message({
            message: '修改成功',
            type: 'success',
            duration: 2000
          })
          this.currentEditId = null
          this.editTypeActive = 'first'
          this.participantList = []
          this.showEditProgramDialog = false
          this.getTrainingProgramList()
        }
      } catch (error) {
        console.log(error)
        return
      }
    },
    handleBeforCloseEditDialog(done) {
      if (done && typeof done === 'function') {
        this.$confirm('确认关闭？关闭后会失去保存的数据', '提示')
          .then((_) => {
            this.editTypeActive = 'first'
            done()
            this.resetForm('editform')
            this.currentEditId = null
            this.participantList = []
          })
          .catch((_) => {})
      } else {
        this.$confirm('确认关闭？关闭后会失去保存的数据', '提示')
          .then((_) => {
            this.editTypeActive = 'first'
            this.showEditProgramDialog = false
            this.resetForm('editform')
            this.currentEditId = null
            this.participantList = []
          })
          .catch((_) => {})
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.header{
  display: flex;
  align-items: center;
}

.transfer-container{
  display:flex;
  justify-content: center;
}
</style>
