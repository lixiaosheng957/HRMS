<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="4">
            <h3>职位管理</h3>
          </el-col>
          <el-col :span="2" :offset="15">
            <el-button type="primary" :icon="showFilter?'el-icon-arrow-up':'el-icon-arrow-down'" @click="showFilter=!showFilter">筛选</el-button>
          </el-col>
          <el-col :span="2">
            <el-button type="primary" icon="el-icon-plus" @click="showAddForm = true">添加职位</el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-row v-show="showFilter" style="margin-bottom:20px">
          <el-col :span="6">
            <el-row>
              <el-col :span="24">
                <el-input v-model="filters.name" type="text" placeholder="根据职位名称搜索" />
              </el-col>
            </el-row>
          </el-col>
          <el-col :span="6" :offset="1">
            <el-row>
              <el-col :span="24">
                <el-select
                  v-model="filters.departmentId"
                  placeholder="请输入关键词"
                  filterable
                  clearable
                  remote
                  :remote-method="getDepartmentsList"
                  :loading="selectLoading"
                >
                  <el-option
                    v-for="item in selectItems"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </el-col>
            </el-row>
          </el-col>
          <el-col :span="6">
            <el-button type="primary" icon="el-icon-search" @click="fetchData(filters)">搜索</el-button>
            <el-button @click="resetFilters">重置</el-button>
          </el-col>
        </el-row>
        <el-table v-loading="listLoading" :data="jobList" border height="550" fit element-loading-text="加载中">
          <el-table-column prop="id" label="职位编号" align="center" width="80" />
          <el-table-column prop="name" label="职位名称" align="center" width="250" />
          <el-table-column prop="titleLevel" label="职位等级" align="center" width="250" />
          <el-table-column prop="number" label="职位人数" align="center" width="120" />
          <el-table-column label="操作" align="center">
            <template slot-scope="scope">
              <el-button type="danger" size="mini" @click="deletJob(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
      <el-dialog title="添加职位" :visible.sync="showAddForm" width="40%">
        <el-form ref="addJobFrom" :model="addForm" :rules="rules">
          <el-form-item label="职位名称" label-width="90px" prop="name">
            <el-input v-model="addForm.name" type="text" placeholder="请输入职位名称" />
          </el-form-item>
          <el-form-item label="职位等级" label-width="90px" prop="titleLevel">
            <el-select v-model="addForm.titleLevel" placeholder="请选择职位等级" clearable>
              <el-option
                v-for="item in titleLevelList"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="所属部门" label-width="90px" prop="departmentId">
            <el-select
              v-model="addForm.departmentId"
              placeholder="请输入关键词"
              filterable
              clearable
              remote
              :remote-method="getDepartmentsList"
              :loading="selectLoading"
            >
              <el-option
                v-for="item in selectItems"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-row>
              <el-col :span="4" :offset="16">
                <el-button type="primary" @click="submitAddForm('addJobFrom')">添加</el-button>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetForm('addJobFrom')">重置</el-button>
              </el-col>
            </el-row>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
import { getJobList, addJob, deleteJob } from '@/api/job'
import { getDepartments } from '@/api/department'
import { Message, MessageBox } from 'element-ui'
export default {
  name: 'Rank',
  data() {
    return {
      jobList: [{
        departmentId: 1,
        enabled: true,
        id: 1,
        name: '人力资源专员',
        titleLevel: '初级'
      }],
      listLoading: false,
      showFilter: false,
      filters: {
        name: null,
        departmentId: null
      },
      selectLoading: false,
      selectItems: [],
      showAddForm: false,
      addForm: {
        name: '',
        titleLevel: '',
        departmentId: null
      },
      titleLevelList: [
        {
          value: '实习',
          label: '实习'
        },
        {
          value: '初级',
          label: '初级'
        },
        {
          value: '中级',
          label: '中级'
        },
        {
          value: '高级',
          label: '高级'
        },
        {
          value: '管理层',
          label: '管理层'
        }
      ],
      rules: {
        name: [
          { required: true, message: '请输入职位名称', trigger: 'blur' }
        ],
        titleLevel: [
          { required: true, message: '请选择职位等级', trigger: 'blur' }
        ],
        departmentId: [
          { required: true, message: '请输入所属部门', trigger: 'blur' }
        ]
      }
    }
  },
  async created() {
    await this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        this.listLoading = true
        if (this.filters.name || this.filters.departmentId) {
          const query = {}
          Object.keys(this.filters).forEach(key => {
            if (this.filters[key]) {
              query[key] = this.filters[key]
            }
          })
          this.jobList = await getJobList(query)
        } else {
          this.jobList = await getJobList()
        }
        this.listLoading = false
      } catch (error) {
        this.listLoading = false
        console.log(error)
      }
    },
    resetFilters() {
      this.filters.name = null
      this.filters.departmentId = null
    },
    async getDepartmentsList(query) {
      if (query) {
        try {
          this.selectLoading = true
          this.selectItems = await getDepartments(
            {
              selectTag: true,
              nameKeyword: query
            }
          )
          this.selectLoading = false
        } catch (error) {
          this.selectLoading = false
          console.log(error)
        }
      } else {
        this.selectItems = []
      }
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    submitAddForm(formName) {
      this.$refs[formName].validate(async(valid) => {
        if (valid) {
          try {
            await addJob(this.addForm)
            Message({
              message: '添加成功',
              type: 'success',
              duration: '2000'
            })
            this.showAddForm = false
            this.resetForm(formName)
            await this.fetchData()
          } catch (error) {
            console.log(error)
          }
        } else {
          return
        }
      })
    },
    deletJob({ id }) {
      MessageBox.confirm('确定要删除吗？', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        try {
          await deleteJob({ id })
          Message({
            message: '删除成功',
            type: 'success',
            duration: '2000'
          })
          await this.fetchData()
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

<style>

</style>
