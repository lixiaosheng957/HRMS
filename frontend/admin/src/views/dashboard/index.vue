<template>
  <div class="dashboard-container">
    <el-row :gutter="12" style="margin-bottom:20px;">
      <el-col :span="18">
        <el-card>
          <employee-info />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <personnel-info />
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="12">
      <el-col :span="8">
        <renew />
      </el-col>
      <el-col :span="8">
        <contract-end />
      </el-col>
      <el-col :span="8">
        <undone-training-program />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import EmployeeInfo from './components/EmployeeInfo'
import PersonnelInfo from './components/PersonnelInfo'
import Renew from './components/Renew'
import ContractEnd from './components/ContractEnd.vue'
import UndoneTrainingProgram from './components/UndoneTrainingProgram.vue'
export default {
  name: 'Dashboard',
  components: { EmployeeInfo, PersonnelInfo, Renew, ContractEnd, UndoneTrainingProgram },
  data() {
    return {
      currentRole: 'adminDashboard'
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    if (this.roles.includes('admin')) {
      this.currentRole = 'adminDashboard'
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>

