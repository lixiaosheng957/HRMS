<template>
  <div class="app-container">
    <el-page-header content="员工详情" @back="goBack" />
    <el-container>
      <el-main>
        <el-tabs v-model="activeName">
          <el-tab-pane label="基础信息" name="first">
            <el-card>
              <div slot="header">
                <span>员工基础信息</span>
              </div>
              <el-form :model="detail" label-width="130px">
                <el-row>
                  <el-col :span="12">
                    <el-form-item label="姓名：">
                      <span>{{ detail.name }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="性别：">
                      <span>{{ detail.gender }}</span>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="12">
                    <el-form-item label="民族：">
                      <span>{{ detail.nation }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="籍贯：">
                      <span>{{ detail.nativePlace }}</span>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="12">
                    <el-form-item label="生日：">
                      <span>{{ detail.birthday }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="婚姻状态：">
                      <span>{{ detail.wedlock }}</span>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="8">
                    <el-form-item label="手机号：">
                      <span>{{ detail.phone }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="邮箱：">
                      <span>{{ detail.email }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="身份证号：">
                      <span>{{ detail.idCard }}</span>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="8">
                    <el-form-item label="毕业学校：">
                      <span>{{ detail.school }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="所学专业：">
                      <span>{{ detail.specialty }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="学历层次：">
                      <span>{{ detail.tipTopDegree }}</span>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="8">
                    <el-form-item label="所属部门：">
                      <span>{{ detail.department }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="职位：">
                      <span>{{ detail.job }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="工号：">
                      <span>{{ detail.workId }}</span>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="12">
                    <el-form-item label="居住地址：">
                      <span>{{ detail.address }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="上家单位：">
                      <span>{{ detail.lastCompany }}</span>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="12">
                    <el-form-item label="合同开始时间：">
                      <span>{{ detail.contractBeginDate }}</span>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="合同结束时间：">
                      <span>{{ detail.contractEndDate }}</span>
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
            </el-card>
          </el-tab-pane>
          <el-tab-pane label="调动经历" name="second">
            <el-card>
              <div slot="header">
                <span>调动记录</span>
              </div>
              <el-timeline :reverse="true">
                <el-timeline-item
                  v-for="(item, index) in detail.transferRecord"
                  :key="index"
                  :timestamp="item.transferTime"
                >
                  <div class="transfer-content">
                    <div class="transfer-type">
                      <span>变动类型：{{ item.transferType }}</span>
                    </div>
                    <div v-if="item.beforeTransferDepartment" class="tranfer-detail">
                      <span>
                        变动内容：{{ item.beforeTransferDepartment }}：{{ item.beforeTransferJob }} <i class="el-icon-right" /> {{ item.transferDepartment }}：{{ item.transferJob }}
                      </span>
                    </div>
                  </div>
                </el-timeline-item>
              </el-timeline>
            </el-card>
          </el-tab-pane>
          <el-tab-pane label="培训经历" name="third">
            <el-card>
              <div slot="header">
                <span>培训记录</span>
              </div>
              <el-timeline :reverse="true">
                <el-timeline-item
                  v-for="(item, index) in detail.trainingRecord"
                  :key="index"
                  :timestamp="item.programStartDate + '  >  '+ item.programEndDate"
                >
                  <div class="transfer-content">
                    <div class="transfer-type">
                      <span>项目名称：{{ item.programName }}</span>
                    </div>
                    <div class="tranfer-detail">
                      <span>
                        培训成绩：{{ item.level }}
                      </span>
                    </div>
                  </div>
                </el-timeline-item>
              </el-timeline>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { getEmployee } from '@/api/employee'
export default {
  name: 'EmployeeDetail',
  data() {
    return {
      currentEmployeeId: null,
      detail: {
        name: '',
        gender: '',
        nation: '',
        nativePlace: '',
        birthday: '',
        wedlock: '',
        phone: '',
        email: '',
        school: '',
        tipTopDegree: '',
        idCard: '',
        department: '',
        job: '',
        address: '',
        lastCompany: '',
        contractBeginDate: '',
        contractEndDate: '',
        transferRecord: [],
        trainingRecord: []
      },
      activeName: 'first'
    }
  },
  created() {
    this.currentEmployeeId = this.$route.params.id
    this.getDetail()
  },
  methods: {
    async getDetail() {
      try {
        this.detail = await getEmployee({ id: this.currentEmployeeId })
      } catch (error) {
        return
      }
    },
    goBack() {
      this.$router.back(-1)
    }
  }
}
</script>

<style lang="scss" scoped>
.transfer-content{
    .transfer-type{
        margin-bottom: 10px;
    }
}
</style>
