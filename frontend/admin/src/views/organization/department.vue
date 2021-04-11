<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="4">
            <h3>部门管理</h3>
          </el-col>
          <el-col :span="2" :offset="16">
            <el-button type="primary" icon="el-icon-plus">添加部门</el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <!-- <el-table :data="departments" border fit height="500" element-loading-text="加载中">
          <el-table-column prop="id" label="部门编号" align="center" width="80" />
          <el-table-column prop="name" label="部门名称" align="center" width="250" />
          <el-table-column prop="depPath" label="办公位置" align="center" width="250" />
          <el-table-column prop="leader" label="部门负责人" align="center" width="150" />
          <el-table-column prop="number" label="人数" align="center" width="150" />
          <el-table-column label="操作" align="center">
            <template>
              <el-button type="primary" size="mini">修改</el-button>
            </template>
          </el-table-column>
        </el-table> -->
        <el-tree :data="departments" default-expand-all />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { getDepartments } from '@/api/department'
export default {
  name: 'Department',
  data() {
    return {
      departments: [],
      departmentsLoading: false,
      defaultProps: {
        children: 'children',
        label: 'label'
      }
    }
  },
  async created() {
    await this.fetchDepartments()
  },
  methods: {
    async fetchDepartments() {
      try {
        this.departmentsLoading = true
        this.departments = await getDepartments()
        this.departmentsLoading = false
      } catch (error) {
        console.log(error)
        this.departmentsLoading = false
      }
    }
  }
}
</script>

<style>

</style>
