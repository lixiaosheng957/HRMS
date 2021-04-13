<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="4">
            <h3>部门管理</h3>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <div class="treeCon clearfix">
          <span>
            <strong>XXX有限公司</strong>
          </span>
          <div class="fr">
            <span class="treeRinfo">
              <div class="treeRinfo">
                <span>负责人</span>
              </div>
              <div class="treeRinfo">
                <el-dropdown @command="handleCommand">
                  <span class="el-dropdown-link">
                    操作
                    <i class="el-icon-arrow-down el-icon--right" />
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item :command="{command:'a',value:null}">添加部门</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </span>
          </div>
        </div>
        <el-tree :data="departments" default-expand-all node-key="id" :expand-on-click-node="false">
          <div slot-scope="{ node,data }" style="width:100%;">
            <span>{{ node.label }}</span>
            <div class="fr">
              <span class="treeRinfo">
                <div class="treeRinfo">
                  <span>{{ data.leader }}</span>
                </div>
                <div class="treeRinfo">
                  <el-dropdown @command="handleCommand">
                    <span class="el-dropdown-link">
                      操作
                      <i class="el-icon-arrow-down el-icon--right" />
                    </span>
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item :command="{command:'b',value:data.id}">添加子部门</el-dropdown-item>
                      <el-dropdown-item :command="{command:'c',value:data.id}">删除部门</el-dropdown-item>
                      <el-dropdown-item :command="{command:'d',value:data.id}">查看部门</el-dropdown-item>
                      <el-dropdown-item :command="{command:'f',value:data.id}">编辑部门</el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>
                </div>
              </span>
            </div>
          </div>
        </el-tree>
      </el-main>
      <el-dialog :title="currentFormTitle" :visible.sync="showDialog" width="40%" @close="closeDialog('departmentForm')">
        <el-form ref="departmentForm" :model="departmentForm" :rules="rules" label-width="90px">
          <el-form-item label="部门名称" required prop="name">
            <el-input v-model="departmentForm.name" type="text" placeholder="请输入部门名称" />
          </el-form-item>
          <el-form-item label="负责人" required prop="leader">
            <el-input v-model="departmentForm.leader" type="text" placeholder="请输入负责人" />
          </el-form-item>
          <el-form-item label="办公位置">
            <el-input v-model="departmentForm.depPath" type="text" placeholder="请输入办公位置" />
          </el-form-item>
          <el-form-item v-show="showAdd||showEdit">
            <el-row>
              <el-col :span="4" :offset="16">
                <el-button type="primary" @click="submitForm('departmentForm')">确定</el-button>
              </el-col>
              <el-col :span="4">
                <el-button @click="closeDialog('departmentForm')">取消</el-button>
              </el-col>
            </el-row>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
import { getDepartments, addDepartment, deleteDepartment, getDepartment, editDepartment } from '@/api/department'
import { Message, MessageBox } from 'element-ui'
export default {
  name: 'Department',
  data() {
    return {
      departments: [],
      departmentsLoading: false,
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      showAdd: false,
      showEdit: false,
      showDetail: false,
      showDialog: false,
      currentOpDepartmentId: null,
      departmentForm: {
        name: '',
        parentId: null,
        depPath: '',
        enabled: true,
        leader: ''
      },
      rules: {
        name: [{ required: true, message: '请输入职位名称', trigger: 'blur' }],
        leader: [{ required: true, message: '请输入负责人', trigger: 'blur' }]
      }
    }
  },
  computed: {
    currentFormTitle: function() {
      if (this.showAdd) {
        return '添加部门'
      }
      if (this.showEdit) {
        return '编辑部门'
      }
      return '查看部门'
    }
  },
  async created() {
    await this.fetchDepartments()
    console.log(this.departments)
  },
  methods: {
    async fetchDepartments() {
      try {
        this.departmentsLoading = true
        this.departments = await getDepartments()
        console.log(this.departments)
        this.departmentsLoading = false
      } catch (error) {
        console.log(error)
        this.departmentsLoading = false
      }
    },
    handleCommand(command) {
      console.log(command)
      if (command.command === 'a') {
        this.handleAddDepartment()
      }
      if (command.command === 'b') {
        this.handleAddChildrenDepartment(command.value)
      }
      if (command.command === 'c') {
        this.handleDeleteDepartment(command.value)
      }
      if (command.command === 'd') {
        this.handleShowDepartment(command.value)
      }
      if (command.command === 'f') {
        this.handleEditDepartment(command.value)
      }
    },
    handleAddDepartment() {
      this.showDialog = true
      this.showAdd = true
      this.currentOpDepartmentId = null
    },
    handleAddChildrenDepartment(id) {
      this.showDialog = true
      this.showAdd = true
      this.currentOpDepartmentId = id
      this.departmentForm.parentId = id
    },
    async handleShowDepartment(id) {
      this.showDetail = true
      this.showDialog = true
      try {
        const result = await getDepartment({ id })
        this.departmentForm.name = result.name
        this.departmentForm.leader = result.leader
        this.departmentForm.depPath = result.depPath
      } catch (error) {
        console.log(error)
      }
    },
    async handleEditDepartment(id) {
      this.showDialog = true
      this.showEdit = true
      this.currentOpDepartmentId = id
      try {
        const result = await getDepartment({ id })
        this.departmentForm.name = result.name
        this.departmentForm.leader = result.leader
        this.departmentForm.depPath = result.depPath
      } catch (error) {
        console.log(error)
      }
    },
    submitForm(formName) {
      this.$refs[formName].validate(async(valid) => {
        if (valid) {
          if (this.showAdd) {
            try {
              const submitObj = {}
              Object.keys(this.departmentForm).forEach(key => {
                if (this.departmentForm[key]) {
                  submitObj[key] = this.departmentForm[key]
                }
              })
              await addDepartment(submitObj)
              Message({
                message: '添加成功',
                type: 'success',
                duration: '2000'
              })
              this.closeDialog('departmentForm')
              await this.fetchDepartments()
            } catch (error) {
              console.log(error)
            }
          }
          if (this.showEdit) {
            try {
              const submitObj = {}
              submitObj.id = this.currentOpDepartmentId
              submitObj.name = this.departmentForm.name
              submitObj.leader = this.departmentForm.leader
              submitObj.depPath = this.departmentForm.depPath
              await editDepartment(submitObj)
              Message({
                message: '修改成功',
                type: 'success',
                duration: '2000'
              })
              this.closeDialog('departmentForm')
              await this.fetchDepartments()
            } catch (error) {
              console.log(error)
            }
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    closeDialog(formName) {
      this.currentOpDepartmentId = null
      this.showAdd = false
      this.showEdit = false
      this.showDetail = false
      this.departmentForm.parentId = null
      this.departmentForm.depPath = ''
      this.departmentForm.enabled = true
      this.$refs[formName].resetFields()
      this.showDialog = false
    },
    handleDeleteDepartment(id) {
      MessageBox.confirm('确定要删除吗？', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        try {
          await deleteDepartment({ id })
          Message({
            message: '删除成功',
            type: 'success',
            duration: '2000'
          })
          await this.fetchDepartments()
        } catch (error) {
          console.log(error)
        }
      }).catch(error => {
        return error
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.treeCon {
    border-bottom: 1px solid #cfcfcf;
    padding: 10px 0;
    margin-bottom: 10px;
}
.treeRinfo{
  display: inline-block;
  span{
    padding-left: 30px;
  }
}

.fr{
  float: right;
}
.el-dropdown-link{
  cursor: pointer;
  color: #409EFF;
}
.clearfix:after {
    visibility: hidden;
    display: block;
    font-size: 0;
    content: " ";
    clear: both;
    height: 0;
}
</style>
