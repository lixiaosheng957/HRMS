<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="4" style="margin-right:10px;">
            <el-input v-model="searchByAccount" placeholder="根据用户名搜索" />
          </el-col>
          <el-col :span="2">
            <el-button type="primary" icon="el-icon-search" @click="fetchData({account:searchByAccount})">搜索</el-button>
          </el-col>
          <el-col :span="4" style="margin-right:10px;">
            <el-select
              v-model="searchByHolder"
              placeholder="根据员工名搜索"
              filterable
              clearable
              remote
              :remote-method="getEmployeeTagsList"
              :loading="selectLoading"
            >
              <el-option
                v-for="item in employeeList"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-col>
          <el-col :span="2">
            <el-button type="primary" icon="el-icon-search" @click="fetchData({holderId:searchByHolder})">搜索</el-button>
          </el-col>
          <el-col :span="3" :offset="8">
            <el-button type="primary" icon="el-icon-plus" @click="showAddForm = true">添加用户</el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-table v-loading="listLoading" :data="userList" border fit height="550px" element-loading-text="加载中">
          <el-table-column prop="id" label="用户编号" align="center" width="80" />
          <el-table-column prop="username" label="用户名" align="center" width="200" />
          <el-table-column prop="holder" label="持有人" align="center" width="120" />
          <el-table-column prop="phone" label="持有人电话" align="center" width="200" />
          <el-table-column label="权限" align="center">
            <template slot-scope="scope">
              <el-popover v-for="(item,index) in scope.row.roles" :key="index" trigger="hover" placement="top">
                <p>权限ID：{{ item.id }}</p>
                <p>权限描述：{{ item.description }}</p>
                <div slot="reference" class="role-wrapper">
                  <el-tag size="medium">{{ item.name }}</el-tag>
                </div>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center">
            <template slot-scope="scope">
              <el-button type="primary" size="mini" @click="handleShowChangePasswordForm(scope.row)">修改</el-button>
              <el-button type="danger" size="mini" :disabled="isAdmin(scope.row)" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
      <el-dialog title="添加用户" :visible.sync="showAddForm" width="40%">
        <el-form ref="addUserForm" :rules="rules" :model="addUserForm">
          <el-form-item label="用户名" label-width="90px" prop="username">
            <el-input v-model="addUserForm.username" type="text" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" label-width="90px" prop="password">
            <el-input v-model="addUserForm.password" type="password" placeholder="请输入密码" />
          </el-form-item>
          <el-form-item label="确认密码" label-width="90px" prop="confirmPassword">
            <el-input v-model="addUserForm.confirmPassword" type="password" placeholder="再次输入密码" />
          </el-form-item>
          <el-form-item label="持有人" label-width="90px" prop="holderId">
            <el-select
              v-model="addUserForm.holderId"
              placeholder="请输入关键词"
              filterable
              clearable
              remote
              :remote-method="getEmployeeTagsList"
              :loading="selectLoading"
            >
              <el-option
                v-for="item in employeeList"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="权限" label-width="90px" prop="roles">
            <el-checkbox-group v-model="addUserForm.roles">
              <el-checkbox label="hr" />
            </el-checkbox-group>
          </el-form-item>
          <el-form-item>
            <el-row>
              <el-col :span="4" :offset="16">
                <el-button type="primary" @click="submitAddForm('addUserForm')">添加</el-button>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetForm('addUserForm')">重置</el-button>
              </el-col>
            </el-row>
          </el-form-item>
        </el-form>
      </el-dialog>
      <el-dialog title="修改密码" :visible.sync="changePwdDialog" width="40%" @close="closeChangePasswordForm">
        <el-form ref="changePasswordForm" :model="changePasswordForm" :rules="rules">
          <el-form-item label="密码" label-width="90px" prop="password">
            <el-input v-model="changePasswordForm.password" type="password" placeholder="请输入密码" />
          </el-form-item>
          <el-form-item label="确认密码" label-width="90px" prop="confirmPassword">
            <el-input v-model="changePasswordForm.confirmPassword" type="password" placeholder="再次输入密码" />
          </el-form-item>
          <el-row>
            <el-col :span="4" :offset="16">
              <el-button type="primary" @click="submitChangePasswordForm('changePasswordForm')">确定</el-button>
            </el-col>
            <el-col :span="4">
              <el-button @click="resetForm('changePasswordForm')">重置</el-button>
            </el-col>
          </el-row>
        </el-form>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
import { getUserList, addUser, changePassword, deleteAccount } from '@/api/user'
import { getEmployeeList } from '@/api/employee'
import { Message } from 'element-ui'
export default {
  name: 'User',
  data() {
    const checkUserName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('用户名不能为空'))
      }
      setTimeout(() => {
        if (value.length < 6) {
          return callback(new Error('用户名长度过短'))
        } else if (value.length > 12) {
          return callback(new Error('用户名长度过长'))
        } else {
          callback()
        }
      }, 1000)
    }
    const checkPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码过短'))
      } else {
        callback()
      }
    }
    const checkConfirmPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.addUserForm.password && this.showAddForm ||
       value !== this.changePasswordForm.password && this.changePwdDialog) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }
    return {
      userList: null,
      selectLoading: false,
      listLoading: false,
      showAddForm: false,
      searchByAccount: '',
      searchByHolder: null,
      addUserForm: {
        username: '',
        password: '',
        confirmPassword: '',
        holderId: null,
        roles: []
      },
      rules: {
        username: [
          {
            validator: checkUserName, trigger: 'blur'
          }
        ],
        password: [
          {
            validator: checkPassword, trigger: 'blur'
          }
        ],
        confirmPassword: [
          {
            validator: checkConfirmPassword, trigger: 'blur'
          }
        ],
        holderId: [
          {
            required: true, message: '请输入持有人', trigger: 'blur'
          }
        ],
        roles: [
          {
            type: 'array', required: true, message: '请选择至少一项权限', trigger: 'change'
          }
        ]
      },
      employeeList: [],
      changePwdDialog: false,
      changePasswordForm: {
        id: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  created() {
    this.fetchData(1, 10)
  },
  methods: {
    async fetchData(query) {
      try {
        this.listLoading = true
        if (query) {
          this.userList = await getUserList(query)
        } else {
          this.userList = await getUserList()
        }
        this.listLoading = false
        console.log(this.userList)
      } catch (error) {
        this.listLoading = false
        console.log(error)
      }
    },
    submitAddForm(formName) {
      this.$refs[formName].validate(async(valid) => {
        if (valid) {
          console.log(this.addUserForm)
          try {
            const submitObj = JSON.parse(JSON.stringify(this.addUserForm))
            const submitRoles = []
            this.addUserForm.roles.forEach(role => {
              const obj = {}
              obj.name = role
              submitRoles.push(obj)
            })
            submitObj.roles = submitRoles
            await addUser(submitObj)
            Message({
              message: '添加成功',
              type: 'success',
              duration: '2000'
            })
            this.showAddForm = false
            this.resetForm(formName)
            this.fetchData()
          } catch (error) {
            console.log(error)
          }
        } else {
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    async getEmployeeTagsList(query) {
      if (query) {
        try {
          this.selectLoading = true
          this.employeeList = await getEmployeeList({ tags: true, name: query })
          this.selectLoading = false
        } catch (error) {
          this.selectLoading = false
          console.log(error)
        }
      }
    },
    isAdmin({ roles }) {
      let flag = false
      roles.forEach(item => {
        if (item.name === 'admin') {
          flag = true
        }
      })
      return flag
    },
    handleShowChangePasswordForm({ id }) {
      this.changePwdDialog = true
      this.changePasswordForm.id = id
    },
    submitChangePasswordForm(formName) {
      this.$refs[formName].validate(async(valid) => {
        if (valid) {
          try {
            const submitObj = {
              id: this.changePasswordForm.id,
              password: this.changePasswordForm.password
            }
            await changePassword(submitObj)
            Message({
              message: '修改成功',
              type: 'success',
              duration: 2000
            })
            this.changePasswordForm.id = null
            this.resetForm(formName)
            this.changePwdDialog = false
            this.fetchData()
          } catch (error) {
            return
          }
        } else {
          return
        }
      })
    },
    closeChangePasswordForm() {
      this.changePasswordForm.id = null
      this.resetForm('changePasswordForm')
    },
    handleDelete({ id }) {
      this.$confirm('确认删除吗,此操作会永久删除', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        await deleteAccount({ id: id })
        Message({
          message: '删除成功',
          type: 'success',
          duration: 2000
        })
        this.fetchData()
      }).catch(_ => {})
    }
  }
}
</script>

<style>

</style>
