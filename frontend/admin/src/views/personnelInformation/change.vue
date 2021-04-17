<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row class="header-row">
          <el-col :span="3">
            <h3>变动记录</h3>
          </el-col>
          <el-col :span="3" :offset="1">
            <el-select
              v-model="searchByName"
              placeholder="根据员工名搜索"
              filterable
              clearable
              remote
              :remote-method="getEmployeeTagsList"
              :loading="searchNameLoading"
            >
              <el-option
                v-for="item in employeeTagsList"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-col>
          <el-col :span="2">
            <el-button type="primary" icon="el-icon-search" @click="search">搜索</el-button>
          </el-col>
          <el-col :span="4" :offset="8">
            <el-switch
              v-model="searchMine"
              active-text="查看我的"
              inactive-text="查看全部"
              @change="filterData"
            />
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-table v-loading="listLoading" :data="recordsList" border fit width="100%" element-loading-text="加载中">
          <el-table-column label="编号" prop="id" width="100" align="center" />
          <el-table-column label="员工姓名" prop="employeeName" width="150" align="center" />
          <el-table-column label="员工工号" prop="employeeWorkId" width="150" align="center" />
          <el-table-column label="操作人" prop="operator" width="150" align="center" />
          <el-table-column label="操作时间" prop="operateTime" width="220" align="center" />
          <el-table-column label="变动类型" prop="transferType" width="150" align="center" />
          <el-table-column label="变动原因" prop="type" width="150" align="center" />
          <el-table-column label="操作" align="center">
            <template slot-scope="scope">
              <el-button type="primary" size="mini" @click="showDetail(scope.row)">查看详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
      <el-dialog title="查看详情" :visible.sync="detailDialog" width="50%">
        <el-card>
          <el-form label-width="150px">
            <el-row>
              <el-col :span="24">
                <h4>调动详情</h4>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="员工姓名">
                  <span>{{ detail.employeeName }}</span>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="员工工号">
                  <span>{{ detail.employeeWorkId }}</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="调动类型">
                  <span>{{ detail.transferType }}</span>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="调动原因类型">
                  <span>{{ detail.type }}</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <el-form-item label="调动具体原因">
                  <span>{{ detail.tips }}</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row v-if="detail.transferDepName">
              <el-col :span="12">
                <el-form-item label="调动后部门">
                  <span>{{ detail.transferDepName }}</span>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="调动前部门">
                  <span>{{ detail.beforeTransferDepName }}</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row v-if="detail.transferJobName">
              <el-col :span="12">
                <el-form-item label="调动后职位">
                  <span>{{ detail.transferJobName }}</span>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="调动前职位">
                  <span>{{ detail.beforeTransferJobName }}</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row v-if="detail.contractBeginDate">
              <el-col :span="12">
                <el-form-item label="变动后合同开始时间">
                  <span>{{ detail.contractBeginDate }}</span>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="变动后合同结束时间">
                  <span>{{ detail.contractEndDate }}</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row v-if="detail.beforeContractBeginDate">
              <el-col :span="12">
                <el-form-item label="变动前合同开始时间">
                  <span>{{ detail.beforeContractBeginDate }}</span>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="变动前合同结束时间">
                  <span>{{ detail.beforeContractEndDate }}</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="调动时间">
                  <span>{{ detail.transferTime }}</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <h4>变动操作详情</h4>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="操作人">
                  <span>{{ detail.operator }}</span>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="操作时间">
                  <span>{{ detail.operateTime }}</span>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-card>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
import { getTransferRecordsList, getTransferDetail, getEmployeeList } from '@/api/employee'
export default {
  name: 'TransferRecord',
  data() {
    return {
      searchByName: '',
      searchNameLoading: false,
      listLoading: false,
      recordsList: [],
      detailDialog: false,
      searchMine: false,
      detail: {
        employeeName: '',
        employeeWorkId: '',
        transferType: '',
        type: '',
        tips: '',
        transferDepName: '',
        transferJobName: '',
        transferTime: null,
        beforeTransferDepName: '',
        beforeTransferJobName: '',
        contractBeginDate: '',
        contractEndDate: '',
        beforeContractBeginDate: '',
        beforeContractEndDate: '',
        operator: '',
        operateTime: ''
      },
      employeeTagsList: null
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async fetchData(params = null) {
      try {
        this.listLoading = true
        if (this.searchMine) {
          params.mine = true
          this.recordsList = await getTransferRecordsList(params)
        } else {
          this.recordsList = await getTransferRecordsList(params)
        }
        console.log(this.recordsList)
        this.listLoading = false
      } catch (error) {
        this.listLoading = false
      }
    },
    async showDetail({ id }) {
      this.detailDialog = true
      try {
        this.detail = await getTransferDetail({ id: id })
      } catch (error) {
        this.detailDialog = false
        console.log(error)
      }
    },
    async getEmployeeTagsList(query) {
      if (query) {
        try {
          this.searchNameLoading = true
          this.employeeTagsList = await getEmployeeList({ tags: true, name: query })
          this.searchNameLoading = false
        } catch (error) {
          this.searchNameLoading = false
          console.log(error)
        }
      }
    },
    search() {
      this.fetchData({ employeeId: this.searchByName })
    },
    filterData() {
      if (this.searchByName) {
        this.fetchData({ employeeId: this.searchByName })
      } else {
        this.filterData()
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.header-row{
  display: flex;
  align-items: center;
}
</style>
