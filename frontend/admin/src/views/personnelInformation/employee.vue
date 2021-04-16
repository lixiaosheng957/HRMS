<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="3">
            <h3>员工管理</h3>
          </el-col>
          <el-col :span="6">
            <el-select
              v-model="searchByName"
              placeholder="名字搜索"
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
            <el-button style="margin-left:10px;" type="primary" icon="el-icon-search" @click="searchBy('name')">搜索</el-button>
          </el-col>
          <el-col :span="6">
            <el-select
              v-model="searchByJob"
              placeholder="根据职位搜索"
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
            <el-button style="margin-left:10px;" type="primary" icon="el-icon-search" @click="searchBy('job')">搜索</el-button>
          </el-col>
          <el-col :span="6">
            <el-select v-model="searchByType" placeholder="选择员工类型">
              <el-option
                v-for="(item,index) in employeeTypeList"
                :key="index"
                :label="item"
                :value="item"
              />
            </el-select>
            <el-button style="margin-left:10px;" type="primary" icon="el-icon-search" @click="searchBy('type')">搜索</el-button>
          </el-col>
          <el-col :span="2" :offset="1">
            <el-button type="primary" icon="el-icon-plus" @click="showAddForm = true">添加员工</el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-container>
        <el-aside width="180px">
          <el-tree ref="tree" :data="departments" default-expand-all :expand-on-click-node="false" node-key="id" highlight-current @node-click="handleClickDepartment" />
        </el-aside>
        <el-main>
          <el-table v-loading="listLoading" :data="employeeList" border height="530" width="100%" fit element-loading-text="加载中">
            <el-table-column prop="id" label="员工编号" align="center" width="80" />
            <el-table-column prop="name" label="员工姓名" align="center" width="150" />
            <el-table-column prop="gender" label="性别" align="center" width="80" />
            <el-table-column prop="phone" label="电话" align="center" width="200" />
            <el-table-column prop="job" label="职位" align="center" width="200" />
            <el-table-column prop="type" label="员工类型" align="center" width="200" />
            <el-table-column label="操作" align="center" fixed="right" width="300">
              <template slot-scope="scope">
                <el-button type="primary" size="mini" round @click="handleEidtEmployee(scope.row)">修改</el-button>
                <el-button type="primary" size="mini" round @click="showDetail(scope.row)">详情</el-button>
                <el-button type="primary" size="mini" round @click="handleShowChangeForm(scope.row)">调动</el-button>
                <el-button type="danger" size="mini" round>离职</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-main>
        <el-dialog title="添加员工" :visible.sync="showAddForm" width="60%" top="2vh">
          <el-form ref="addEmployeeForm" :model="addEmployeeForm" label-width="100px" :rules="rules">
            <el-row>
              <el-col :span="12">
                <el-form-item label="姓名" prop="name">
                  <el-input v-model="addEmployeeForm.name" type="text" placeholder="请输入员工姓名" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="性别" prop="gender">
                  <el-radio v-model="addEmployeeForm.gender" label="男">男</el-radio>
                  <el-radio v-model="addEmployeeForm.gender" label="女">女</el-radio>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="民族" prop="nation">
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
                <el-form-item label="籍贯" prop="nativePlace">
                  <el-input v-model="addEmployeeForm.nativePlace" type="text" placeholder="请输入籍贯" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="生日" prop="birthday">
                  <el-date-picker v-model="addEmployeeForm.birthday" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="婚姻状态" prop="wedlock">
                  <el-radio v-model="addEmployeeForm.wedlock" label="未婚" />
                  <el-radio v-model="addEmployeeForm.wedlock" label="已婚" />
                  <el-radio v-model="addEmployeeForm.wedlock" label="离异" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="手机号" prop="phone">
                  <el-input
                    v-model="addEmployeeForm.phone"
                    type="text"
                    placeholder="请输入手机号"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="邮箱" prop="email">
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
                <el-form-item label="毕业学校" prop="school">
                  <el-input
                    v-model="addEmployeeForm.school"
                    type="text"
                    placeholder="请输入毕业学校"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="所学专业" prop="specialty">
                  <el-input
                    v-model="addEmployeeForm.specialty"
                    type="text"
                    placeholder="请输入专业"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="学历层次" prop="tipTopDegree">
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
              <el-col :span="8">
                <el-form-item label="工作时间" prop="workAge">
                  <el-input-number v-model="addEmployeeForm.workAge" :step="0.5" :min="0" size="small" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="身份证号" prop="idCard">
                  <el-input v-model="addEmployeeForm.idCard" type="text" placeholder="请输入身份证号" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="工号" prop="workId">
                  <el-input v-model="addEmployeeForm.workId" type="text" placeholder="请输入工号" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">
                <el-form-item label="所属部门" prop="departmentId">
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
              <el-col :span="8">
                <el-form-item label="职位" prop="jobLevelId">
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
              <el-col :span="8">
                <el-form-item label="员工类型" prop="type">
                  <el-select v-model="addEmployeeForm.type" placeholder="请选择民族">
                    <el-option
                      v-for="(item,index) in employeeTypeList"
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
                <el-form-item label="居住地址" prop="address">
                  <el-input v-model="addEmployeeForm.address" type="text" placeholder="请输入住址" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="上家单位">
                  <el-input v-model="addEmployeeForm.lastCompany" type="text" placeholder="请输入住址" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="合同开始时间" :prop="addEmployeeForm.type!=='实习员工'&&addEmployeeForm.type?'contractBeginDate':''">
                  <el-date-picker v-model="addEmployeeForm.contractBeginDate" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="合同结束时间" :prop="addEmployeeForm.type!=='实习员工'&&addEmployeeForm.type?'contractEndDate':''">
                  <el-date-picker v-model="addEmployeeForm.contractEndDate" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="4" :offset="16">
                <el-button type="primary" @click="submitForm('addEmployeeForm')">提交</el-button>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetForm('addEmployeeForm')">重置</el-button>
              </el-col>
            </el-row>
          </el-form>
        </el-dialog>
        <el-dialog title="修改基础信息" :visible.sync="showEditForm" width="40%" top="10vh">
          <el-form ref="editEmployeeForm" :model="editEmployeeForm" label-width="90px" :rules="rules">
            <el-form-item label="婚姻状况" prop="wedlock">
              <el-radio v-model="editEmployeeForm.wedlock" label="未婚" />
              <el-radio v-model="editEmployeeForm.wedlock" label="已婚" />
              <el-radio v-model="editEmployeeForm.wedlock" label="离异" />
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input
                v-model="editEmployeeForm.phone"
                type="text"
                placeholder="请输入手机号"
              />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input
                v-model="editEmployeeForm.email"
                type="text"
                placeholder="请输入邮箱"
              />
            </el-form-item>
            <el-form-item label="居住地址" prop="address">
              <el-input v-model="editEmployeeForm.address" type="text" placeholder="请输入住址" />
            </el-form-item>
            <el-row>
              <el-col :span="4" :offset="16">
                <el-button type="primary" @click="submitForm('editEmployeeForm')">提交</el-button>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetForm('editEmployeeForm')">重置</el-button>
              </el-col>
            </el-row>
          </el-form>
        </el-dialog>
        <el-dialog title="员工调动" :visible.sync="showChangeForm" width="40%" top="10vh">
          <el-form ref="transferForm" :model="transferForm" :rules="transferFormRules" label-width="150px">
            <el-row>
              <el-col :span="12">
                <el-form-item label="职位变动类型" prop="transferType">
                  <el-select v-model="transferForm.transferType" placeholder="请选择">
                    <el-option
                      v-for="(item,index) in transferTypeList"
                      :key="index"
                      :label="item"
                      :value="item"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="变动原因类型" prop="type">
                  <el-select v-model="transferForm.type" placeholder="请选择">
                    <el-option label="主动申请" value="主动申请" />
                    <el-option label="上级要求" value="上级要求" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="变动后部门" :prop="transferForm.transferType === '职位变动' || transferForm.transferType === '实习转试用'?'transferDepartmentId':''">
              <el-select
                v-model="transferForm.transferDepartmentId"
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
            <el-form-item label="变动后职位" :prop="transferForm.transferType === '职位变动' || transferForm.transferType === '实习转试用'?'transferJobId':''">
              <el-select
                v-model="transferForm.transferJobId"
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
            <el-form-item label="变动后合同开始时间" :prop="transferForm.transferType === '实习转试用' || transferForm.contractEndDate?'contractBeginDate':''">
              <el-date-picker v-model="transferForm.contractBeginDate" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
            </el-form-item>
            <el-form-item label="变动后合同结束时间" :prop="transferForm.transferType === '实习转试用' || transferForm.contractBeginDate?'contractEndDate':''">
              <el-date-picker v-model="transferForm.contractEndDate" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
            </el-form-item>
            <el-form-item label="调动日期" prop="transferTime">
              <el-date-picker v-model="transferForm.transferTime" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
            </el-form-item>
            <el-form-item label="变动具体原因" prop="tips">
              <el-input v-model="transferForm.tips" type="textarea" placeholder="请输入具体原因" :rows="4" show-word-limit :maxlength="255" />
            </el-form-item>
            <el-row>
              <el-col :span="4" :offset="16">
                <el-button type="primary" @click="submitForm('transferForm')">确定</el-button>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetForm('transferForm')">重置</el-button>
              </el-col>
            </el-row>
          </el-form>
        </el-dialog>
        <el-drawer title="员工详情" :visible.sync="showDetailView" direction="rtl" size="30%">
          <div class="detail-container">
            <el-form label-width="100px">
              <el-form-item label="姓名">
                <span>{{ deatil.name }}</span>
              </el-form-item>
              <el-form-item label="性别">
                <span>{{ deatil.gender }}</span>
              </el-form-item>
              <el-form-item label="民族">
                <span>{{ deatil.nation }}</span>
              </el-form-item>
              <el-form-item label="籍贯">
                <span>{{ deatil.nativePlace }}</span>
              </el-form-item>
              <el-form-item label="生日">
                <span>{{ deatil.birthday }}</span>
              </el-form-item>
              <el-form-item label="身份证号">
                <span>{{ deatil.idCard }}</span>
              </el-form-item>
              <el-form-item label="婚姻状况">
                <span>{{ deatil.wedlock }}</span>
              </el-form-item>
              <el-form-item label="邮箱">
                <span>{{ deatil.email }}</span>
              </el-form-item>
              <el-form-item label="手机号">
                <span>{{ deatil.phone }}</span>
              </el-form-item>
              <el-form-item label="学历">
                <span>{{ deatil.tipTopDegree }}</span>
              </el-form-item>
              <el-form-item label="毕业院校">
                <span>{{ deatil.school }}</span>
              </el-form-item>
              <el-form-item label="所学专业">
                <span>{{ deatil.specialty }}</span>
              </el-form-item>
              <el-form-item label="参加工作时间">
                <span>{{ deatil.workAge }}年</span>
              </el-form-item>
              <el-form-item label="在岗状态">
                <span>{{ deatil.workState }}</span>
              </el-form-item>
              <el-form-item label="所属部门">
                <span>{{ deatil.department }}</span>
              </el-form-item>
              <el-form-item label="职位">
                <span>{{ deatil.job }}</span>
              </el-form-item>
              <el-form-item label="工号">
                <span>{{ deatil.workId }}</span>
              </el-form-item>
              <el-form-item label="居住地址">
                <span>{{ deatil.address }}</span>
              </el-form-item>
              <el-form-item label="上家单位">
                <span>{{ deatil.lastCompany }}</span>
              </el-form-item>
              <el-form-item label="合同开始时间">
                <span>{{ deatil.contractBeginDate }}</span>
              </el-form-item>
              <el-form-item label="合同结束时间">
                <span>{{ deatil.contractEndDate }}</span>
              </el-form-item>
            </el-form>
          </div>
        </el-drawer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { getEmployeeList, addEmployee, getEmployee, editEmployee, transfer } from '@/api/employee'
import { tipTopDegree, nation, employeeType, transferType } from '@/utils/infoList'
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
      searchByName: '',
      searchByJob: '',
      searchByType: '',
      searchNameLoading: false,
      departments: [],
      currentFilterDepartmentKey: null,
      showAddForm: false,
      showEditForm: false,
      showDetailView: false,
      showChangeForm: false,
      addEmployeeForm: {
        name: '',
        gender: '',
        nation: '',
        nativePlace: '',
        birthday: null,
        idCard: '',
        email: '',
        wedlock: '',
        workId: '',
        phone: '',
        workAge: null,
        tipTopDegree: '',
        school: '',
        specialty: '',
        type: '',
        workState: '在职',
        departmentId: null,
        jobLevelId: null,
        address: '',
        contractBeginDate: null,
        contractEndDate: null,
        lastCompany: ''
      },
      rules: {
        name: [{ required: true, message: '员工姓名不能为空', trigger: 'blur' }],
        gender: [{ required: true, message: '请选择员工性别', trigger: 'blur' }],
        nation: [{ required: true, message: '请选择民族', trigger: 'blur' }],
        nativePlace: [{ required: true, message: '籍贯不能为空', trigger: 'blur' }],
        birthday: [{ required: true, message: '请选择生日', trigger: 'blur' }],
        wedlock: [{ required: true, message: '请选择婚姻状态', trigger: 'blur' }],
        phone: [{ validator: checkPhone, trigger: 'blur', required: true }],
        email: [{ validator: checkEmail, trigger: 'blur', required: true }],
        school: [{ required: true, message: '毕业院校不能为空', trigger: 'blur' }],
        specialty: [{ required: true, message: '专业不能为空', trigger: 'blur' }],
        tipTopDegree: [{ required: true, message: '学历不能为空', trigger: 'blur' }],
        workAge: [{ required: true, message: '工作时间不能为空', trigger: 'blur' }],
        idCard: [{ validator: checkIdCard, trigger: 'blur', required: true }],
        workId: [{ required: true, message: '工号不能为空', trigger: 'blur' }],
        type: [{ required: true, message: '员工类型不能为空', trigger: 'blur' }],
        departmentId: [{ required: true, message: '所属部门不能为空', trigger: 'blur' }],
        jobLevelId: [{ required: true, message: '职位不能为空', trigger: 'blur' }],
        address: [{ required: true, message: '居住地址不能为空', trigger: 'blur' }],
        contractBeginDate: [{ required: true, message: '合同开始时间不能为空', trigger: 'blur' }],
        contractEndDate: [{ required: true, message: '合同结束时间不能为空', trigger: 'blur' }]
      },
      editEmployeeForm: {
        id: null,
        wedlock: '',
        phone: '',
        email: '',
        address: ''
      },
      nationList: nation,
      tipTopDegreeList: tipTopDegree,
      employeeTypeList: employeeType,
      departmentSelectList: null,
      jobSelectList: null,
      deatil: {
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
        department: '',
        job: '',
        workId: '',
        address: '',
        lastCompany: '',
        contractBeginDate: '',
        contractEndDate: ''
      },
      transferForm: {
        employeeId: null,
        transferType: '',
        type: '',
        transferTime: null,
        transferDepartmentId: null,
        transferJobId: '',
        contractBeginDate: '',
        contractEndDate: '',
        tips: ''
      },
      transferTypeList: transferType,
      transferFormRules: {
        transferType: [{ required: true, message: '变动类型不能为空', trigger: 'blur' }],
        type: [{ required: true, message: '变动原因类型不能为空', trigger: 'blur' }],
        transferTime: [{ required: true, message: '变动时间不能为空', trigger: 'blur' }],
        tips: [{ required: true, message: '具体原因不能为空', trigger: 'blur' }],
        transferDepartmentId: [{ required: true, message: '变动后部门不能为空', trigger: 'blur' }],
        transferJobId: [{ required: true, message: '变动后职位不能为空', trigger: 'blur' }],
        contractBeginDate: [{ required: true, message: '变动后合同开始时间不能为空', trigger: 'blur' }],
        contractEndDate: [{ required: true, message: '变动后合同结束时间不能为空', trigger: 'blur' }]
      },
      employeeTagsList: null
    }
  },
  async created() {
    await this.getDepartmentsFilter()
    await this.fetchData({ departmentId: 1 })
    this.$nextTick(() => {
      this.$refs.tree.setCurrentKey(1)
      this.currentFilterDepartmentKey = 1
    })
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
          if (this.addEmployeeForm.departmentId || this.transferForm.transferDepartmentId) {
            this.jobSelectList = await getJobList({
              name: query,
              departmentId: this.addEmployeeForm.departmentId || this.transferForm.transferDepartmentId,
              tags: true
            })
          } else {
            this.jobSelectList = await getJobList({
              name: query,
              tags: true
            })
          }
          this.searchJobLoading = false
          console.log(this.jobSelectList)
        } catch (error) {
          this.searchJobLoading = false
          console.log(error)
        }
      }
    },
    async handleClickDepartment(data) {
      try {
        await this.fetchData({
          departmentId: data.id
        })
        this.currentFilterDepartmentKey = data.id
      } catch (error) {
        console.log(error)
      }
    },
    currentFilterDepartment(key) {
      console.log(key)
    },
    submitForm(formName) {
      this.$refs[formName].validate(async(valid) => {
        if (valid) {
          if (this.showAddForm) {
            try {
              await addEmployee(this.addEmployeeForm)
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
          }
          if (this.showEditForm) {
            try {
              await editEmployee(this.editEmployeeForm)
              Message({
                message: '修改成功',
                type: 'success',
                duration: '2000'
              })
              this.showEditForm = false
              this.resetForm(formName)
              this.editEmployeeForm.id = null
              this.fetchData()
            } catch (error) {
              console.log(error)
            }
          }
          if (this.showChangeForm) {
            try {
              const submitObj = {}
              Object.keys(this.transferForm).forEach(key => {
                if (this.transferForm[key]) {
                  submitObj[key] = this.transferForm[key]
                }
              })
              await transfer(submitObj)
              Message({
                message: '变动成功',
                type: 'success',
                duration: '2000'
              })
              this.showChangeForm = false
              this.resetForm(formName)
              this.transferForm.employeeId = null
              this.fetchData()
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
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    async handleEidtEmployee({ id }) {
      this.showEditForm = true
      try {
        const res = await getEmployee({ id })
        Object.keys(this.editEmployeeForm).forEach(key => {
          this.editEmployeeForm[key] = res[key]
        })
        this.editEmployeeForm.id = id
      } catch (error) {
        console.log(error)
      }
    },
    async showDetail({ id }) {
      console.log(this.$refs.tree.getCurrentKey())
      this.showDetailView = true
      try {
        this.deatil = await getEmployee({ id })
      } catch (error) {
        console.log(error)
      }
    },
    handleShowChangeForm({ id }) {
      this.showChangeForm = true
      this.transferForm.employeeId = id
    },
    async searchBy(keyword) {
      if (keyword === 'name') {
        if (this.searchByName) {
          await this.fetchData({
            departmentId: this.currentFilterDepartmentKey,
            id: this.searchByName
          })
          this.searchByName = null
        }
      }
      if (keyword === 'job') {
        console.log(keyword)
        if (this.searchByJob) {
          await this.fetchData({
            departmentId: this.currentFilterDepartmentKey,
            jobId: this.searchByJob
          })
          this.searchByJob = null
        }
      }
      if (keyword === 'type') {
        if (this.searchByType) {
          await this.fetchData({
            departmentId: this.currentFilterDepartmentKey,
            type: this.searchByType
          })
          this.searchByType = null
        }
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
    handleEmployeeMove() {

    }
  }
}
</script>

<style lang="scss" scoped>
.detail-container{
  height: calc(100vh - 44.4px);
  overflow: scroll;
}
</style>
