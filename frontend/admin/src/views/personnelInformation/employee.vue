<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="4">
            <h3>正式员工</h3>
          </el-col>
          <el-col :span="2" :offset="15">
            <el-button type="primary" :icon="showFilter?'el-icon-arrow-up':'el-icon-arrow-down'" @click="showFilter = !showFilter">筛选</el-button>
          </el-col>
          <el-col :span="2">
            <el-button type="primary" icon="el-icon-plus" @click="showAddForm = true">添加</el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-container>
        <el-aside width="180px">
          <el-tree :data="departments" default-expand-all @node-click="handleClickDepartment" />
        </el-aside>
        <el-main>
          <el-table v-loading="listLoading" :data="employeeList" border height="500" fit element-loading-text="加载中">
            <el-table-column prop="id" label="员工编号" align="center" width="80" />
            <el-table-column prop="name" label="员工姓名" align="center" width="150" />
            <el-table-column prop="gender" label="性别" align="center" width="80" />
            <el-table-column prop="phone" label="电话" align="center" width="200" />
            <el-table-column prop="job" label="职位" align="center" width="200" />
            <el-table-column label="操作" align="center">
              <template>
                <el-button type="primary" size="mini">修改</el-button>
                <el-button type="primary" size="mini">详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-main>
        <el-dialog title="添加员工" :visible.sync="showAddForm" width="50%">
          <el-form ref="addEmployeeForm" :model="addEmployeeForm" label-width="90px" :rules="rules">
            <el-row>
              <el-col :span="12">
                <el-form-item label="姓名" required prop="name">
                  <el-input v-model="addEmployeeForm.name" type="text" placeholder="请输入员工姓名" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="性别" prop="gender" required>
                  <el-radio v-model="addEmployeeForm.gender" label="男">男</el-radio>
                  <el-radio v-model="addEmployeeForm.gender" label="女">女</el-radio>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="民族" required prop="nation">
                  <el-select v-model="addEmployeeForm.nation" placeholder="请选择民族">
                    <el-option
                      v-for="(item,index) in nationList"
                      :key="index"
                      :label="item"
                      :value="item"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="籍贯" required prop="nativePlace">
                  <el-input v-model="addEmployeeForm.nativePlace" type="text" placeholder="请输入籍贯" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="生日" required prop="birthday">
                  <el-date-picker v-model="addEmployeeForm.birthday" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="婚姻状态" required prop="wedlock">
                  <el-radio v-model="addEmployeeForm.wedlock" label="未婚" />
                  <el-radio v-model="addEmployeeForm.wedlock" label="已婚" />
                  <el-radio v-model="addEmployeeForm.wedlock" label="离异" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="手机号" required prop="phone">
                  <el-input
                    v-model="addEmployeeForm.phone"
                    type="text"
                    placeholder="请输入手机号"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="邮箱" required prop="email">
                  <el-input
                    v-model="addEmployeeForm.email"
                    type="text"
                    placeholder="请输入邮箱"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">
                <el-form-item label="毕业学校" required prop="school">
                  <el-input
                    v-model="addEmployeeForm.school"
                    type="text"
                    placeholder="请输入毕业学校"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="所学专业" required prop="specialty">
                  <el-input
                    v-model="addEmployeeForm.specialty"
                    type="text"
                    placeholder="请输入专业"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="学历层次" required prop="tipTopDegree">
                  <el-select v-model="addEmployeeForm.tipTopDegree" placeholder="请选择">
                    <el-option
                      v-for="(item,index) in tipTopDegreeList"
                      :key="index"
                      :label="item"
                      :value="item"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="工作时间">
                  <el-input-number v-model="addEmployeeForm.workAge" :step="0.5" :min="0" size="small" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="身份证号">
                  <el-input v-model="addEmployeeForm.idCard" type="text" placeholder="请输入身份证号" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="所属部门">
                  <el-select
                    v-model="addEmployeeForm.departmentId"
                    placeholder="请输入关键词"
                    filterable
                    clearable
                    remote
                    :remote-method="getDepartmentsTagsList"
                    :loading="searchDepartmentLoading"
                  >
                    <el-option
                      v-for="item in departmentSelectList"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="职位">
                  <el-select
                    v-model="addEmployeeForm.jobLevelId"
                    placeholder="请输入关键词"
                    filterable
                    clearable
                    remote
                    :remote-method="getJobTagsList"
                    :loading="searchJobLoading"
                  >
                    <el-option
                      v-for="item in jobSelectList"
                      :key="item.label"
                      :label="item.label"
                      :value="item.value"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="4" :offset="16">
                <el-button type="primary" @click="submitAddEmployee('addEmployeeForm')">提交</el-button>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetForm('addEmployeeForm')">重置</el-button>
              </el-col>
            </el-row>
          </el-form>
        </el-dialog>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { getEmployeeList, addEmployee } from '@/api/employee'
import { tipTopDegree, nation } from '@/utils/infoList'
import { getDepartments } from '@/api/department'
import { getJobList } from '@/api/job'
import { validPhone, validEmail, validIdCard } from '@/utils/validate'
import { Message } from 'element-ui'
export default {
  name: 'Employee',
  data() {
    const checkPhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入持有人电话'))
      } else if (!validPhone(value)) {
        console.log(validPhone(value))
        callback(new Error('电话号码格式错误'))
      } else {
        callback()
      }
    }
    const checkEmail = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入邮箱'))
      } else if (!validEmail(value)) {
        callback(new Error('邮箱格式错误'))
      } else {
        callback()
      }
    }
    const checkIdCard = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入身份证'))
      } else if (!validIdCard(value).code) {
        callback(new Error('身份证号格式不正确'))
      } else {
        callback()
      }
    }
    return {
      listLoading: false,
      searchDepartmentLoading: false,
      searchJobLoading: false,
      employeeList: [],
      departments: [],
      showFilter: false,
      showAddForm: false,
      addEmployeeForm: {
        name: '',
        gender: '',
        nation: '',
        nativePlace: '',
        birthday: null,
        idCard: '',
        email: '',
        wedlock: '',
        phone: '',
        workAge: null,
        tipTopDegree: '',
        school: '',
        specialty: '',
        type: '正式员工',
        workState: '在职',
        departmentId: null,
        jobLevelId: null
      },
      rules: {
        name: [{ required: true, message: '员工姓名不能为空', trigger: 'blur' }],
        gender: [{ required: true, message: '请选择员工性别', trigger: 'blur' }],
        nation: [{ required: true, message: '请选择民族', trigger: 'blur' }],
        nativePlace: [{ required: true, message: '籍贯不能为空', trigger: 'blur' }],
        birthday: [{ required: true, message: '请选择生日', trigger: 'blur' }],
        wedlock: [{ required: true, message: '请选择婚姻状态', trigger: 'blur' }],
        phone: [{ validator: checkPhone, trigger: 'blur' }],
        email: [{ validator: checkEmail, trigger: 'blur' }],
        school: [{ required: true, message: '毕业院校不能为空', trigger: 'blur' }],
        specialty: [{ required: true, message: '专业不能为空', trigger: 'blur' }],
        tipTopDegree: [{ required: true, message: '学历不能为空', trigger: 'blur' }],
        workAge: [{ required: true, message: '工作时间不能为空', trigger: 'blur' }],
        idCard: [{ validator: checkIdCard, trigger: 'blur' }],
        departmentId: [{ required: true, message: '所属部门不能为空', trigger: 'blur' }],
        jobLevelId: [{ required: true, message: '职位不能为空', trigger: 'blur' }]
      },
      nationList: nation,
      tipTopDegreeList: tipTopDegree,
      departmentSelectList: [],
      jobSelectList: []
    }
  },
  async created() {
    await this.fetchData({ type: '正式员工' })
    await this.getDepartmentsFilter()
  },
  methods: {
    async fetchData(params) {
      try {
        this.listLoading = true
        this.employeeList = await getEmployeeList(params)
        this.listLoading = false
      } catch (error) {
        this.listLoading = false
        console.log(error)
      }
    },
    async getDepartmentsFilter() {
      try {
        this.departments = await getDepartments()
      } catch (error) {
        console.log(error)
      }
    },
    async getDepartmentsTagsList(query) {
      if (query) {
        try {
          this.searchDepartmentLoading = true
          this.departmentSelectList = await getDepartments({
            selectTag: true,
            nameKeyword: query
          })
          this.searchDepartmentLoading = false
        } catch (error) {
          this.searchDepartmentLoading = false
          console.log(error)
        }
      }
    },
    async getJobTagsList(query) {
      console.log(this.addEmployeeForm.departmentId)
      if (query) {
        try {
          this.searchJobLoading = true
          this.jobSelectList = await getJobList({
            name: query,
            departmentId: this.addEmployeeForm.departmentId,
            tags: true
          })
          this.searchJobLoading = false
          console.log(this.jobSelectList)
        } catch (error) {
          this.searchJobLoading = false
          console.log(error)
        }
      }
    },
    async handleClickDepartment(data) {
      console.log(data.id)
      try {
        await this.fetchData({
          type: '正式员工',
          departmentId: data.id
        })
      } catch (error) {
        console.log(error)
      }
    },
    submitAddEmployee(formNmae) {
      console.log(this.addEmployeeForm)
      this.$refs[formNmae].validate(async(valid) => {
        if (valid) {
          try {
            await addEmployee(this.addEmployeeForm)
            Message({
              message: '添加成功',
              type: 'success',
              duration: '2000'
            })
            this.showAddForm = false
            this.resetForm(formNmae)
          } catch (error) {
            console.log(error)
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style>

</style>
