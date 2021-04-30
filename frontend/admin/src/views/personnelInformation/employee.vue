<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="3">
            <h3>员工管理</h3>
          </el-col>
          <el-col :span="4" :offset="1">
            <el-select
              v-model="query.id"
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
          </el-col>
          <el-col :span="4">
            <el-select
              v-model="query.jobId"
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
          </el-col>
          <el-col :span="4">
            <el-select v-model="query.type" clearable placeholder="选择员工类型">
              <el-option
                v-for="(item,index) in employeeTypeList"
                :key="index"
                :label="item"
                :value="item"
              />
            </el-select>
          </el-col>
          <el-col :span="2">
            <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
          </el-col>
          <el-col :span="2" :offset="1">
            <el-button type="primary" icon="el-icon-plus" @click="showAddForm = true">添加员工</el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-container>
        <el-aside width="180px">
          <el-tree ref="tree" :data="departments" default-expand-all :expand-on-click-node="false" node-key="id" :highlight-current="!isSearch" @node-click="handleClickDepartment" />
        </el-aside>
        <el-main>
          <el-table v-loading="listLoading" :data="employeeList" border height="560" width="100%" fit element-loading-text="加载中">
            <el-table-column prop="id" label="员工编号" align="center" width="80" />
            <el-table-column prop="name" label="员工姓名" align="center" width="150" />
            <el-table-column prop="phone" label="电话" align="center" width="150" />
            <el-table-column prop="job" label="职位" align="center" width="200" />
            <el-table-column prop="type" label="员工类型" align="center" width="200" />
            <el-table-column label="操作" align="center" fixed="right" width="420">
              <template slot-scope="scope">
                <el-button type="primary" size="mini" round :disabled="scope.row.type!=='正式员工'" @click="handleShowRenew(scope.row)">续约</el-button>
                <el-button type="primary" size="mini" round @click="handleEidtEmployee(scope.row)">修改</el-button>
                <el-button type="primary" size="mini" round @click="geToDetailView(scope.row)">详情</el-button>
                <el-button type="primary" size="mini" round @click="handleShowChangeForm(scope.row)">调动</el-button>
                <el-button type="danger" size="mini" round @click="handleEmployeeMove(scope.row)">离职</el-button>
                <el-button v-if="isAdmin()" type="danger" size="mini" round @click="handleDelete(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-main>
        <el-dialog title="添加员工" :visible.sync="showAddForm" width="60%" top="2vh">
          <el-form ref="addEmployeeForm" :model="addEmployeeForm" label-width="100px" :rules="rules">
            <el-row>
              <el-col :span="8">
                <el-form-item label="姓名" prop="name">
                  <el-input v-model="addEmployeeForm.name" type="text" placeholder="请输入员工姓名" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="性别" prop="gender">
                  <el-radio v-model="addEmployeeForm.gender" label="男">男</el-radio>
                  <el-radio v-model="addEmployeeForm.gender" label="女">女</el-radio>
                </el-form-item>
              </el-col>
              <el-col :span="8">
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
            </el-row>
            <el-row>
              <el-col :span="8">
                <el-form-item label="籍贯" prop="nativePlace">
                  <el-input v-model="addEmployeeForm.nativePlace" type="text" placeholder="请输入籍贯" />
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
              <el-col :span="10">
                <el-form-item label="生日" prop="birthday">
                  <el-date-picker v-model="addEmployeeForm.birthday" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="居住地址" prop="address">
                  <el-input v-model="addEmployeeForm.address" type="text" placeholder="请输入住址" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">
                <el-form-item label="手机号" prop="phone">
                  <el-input
                    v-model="addEmployeeForm.phone"
                    type="text"
                    placeholder="请输入手机号"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="邮箱" prop="email">
                  <el-input
                    v-model="addEmployeeForm.email"
                    type="text"
                    placeholder="请输入邮箱"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="上家单位">
                  <el-input v-model="addEmployeeForm.lastCompany" type="text" placeholder="请输入上家单位" />
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
              <el-col :span="8">
                <el-form-item label="入职时间" prop="joinDate">
                  <el-date-picker v-model="addEmployeeForm.joinDate" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
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
        <el-dialog title="员工调动" :visible.sync="showChangeForm" width="40%" top="10vh" @close="resetForm('transferForm')">
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
        <el-dialog title="员工离职" :visible.sync="showMoveForm">
          <el-form ref="employeeMoveForm" :model="employeeMoveForm" :rules="moveFormRules" label-width="90px">
            <el-form-item label="离职原因" prop="reason">
              <el-input v-model="employeeMoveForm.reason" type="textarea" placeholder="请输入离职原因" />
            </el-form-item>
            <el-form-item label="离职时间" prop="moveTime">
              <el-date-picker v-model="employeeMoveForm.moveTime" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
            </el-form-item>
            <el-row>
              <el-col :span="4" :offset="16">
                <el-button type="primary" @click="submitForm('employeeMoveForm')">确定</el-button>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetForm('employeeMoveForm')">重置</el-button>
              </el-col>
            </el-row>
          </el-form>
        </el-dialog>
        <el-dialog title="员工续约" :visible.sync="renewDialog" @close="closeRenewDialog">
          <el-form ref="renewForm" :model="renewForm" :rules="rules" label-width="130px">
            <el-row>
              <el-col :span="24">
                <el-form-item label="上次合同开始时间">
                  <el-date-picker v-model="renewForm.beforeContractBeginDate" :disabled="true" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
                  <i class="el-icon-arrow-right" style="font-size:20px; margin-left:10px; margin-right:10px;" />
                  <el-date-picker v-model="renewForm.beforeContractEndDate" :disabled="true" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item label="合同开始时间" prop="contractBeginDate">
                  <el-date-picker v-model="renewForm.contractBeginDate" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="合同结束时间" prop="contractEndDate">
                  <el-date-picker v-model="renewForm.contractEndDate" type="date" placeholder="选择日期" value-format="yyyy-MM-dd" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="4" :offset="16">
                <el-button type="primary" @click="submitForm('renewForm')">提交</el-button>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetForm('renewForm')">重置</el-button>
              </el-col>
            </el-row>
          </el-form>
        </el-dialog>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getEmployeeList,
  addEmployee,
  getEmployee,
  editEmployee,
  transfer,
  employeeMove,
  employeeRenew,
  deleteEmployee
} from '@/api/employee'
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
      } else if (validIdCard(value).code === -1) {
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
      isSearch: false,
      query: {
        id: null,
        jobId: null,
        type: ''
      },
      searchNameLoading: false,
      departments: [],
      currentFilterDepartmentKey: 1,
      showAddForm: false,
      showEditForm: false,
      showChangeForm: false,
      showMoveForm: false,
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
        lastCompany: '',
        joinDate: null
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
        contractEndDate: [{ required: true, message: '合同结束时间不能为空', trigger: 'blur' }],
        joinDate: [{ required: true, message: '入职时间不能为空', trigger: 'blur' }]
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
      employeeTagsList: null,
      employeeMoveForm: {
        employeeId: null,
        reason: '',
        moveTime: null
      },
      moveFormRules: {
        reason: [{ required: true, message: '离职原因不能为空', trigger: 'blur' }],
        moveTime: [{ required: true, message: '离职时间不能为空', trigger: 'blur' }]
      },
      renewDialog: false,
      renewForm: {
        employeeId: null,
        beforeContractBeginDate: null,
        beforeContractEndDate: null,
        contractBeginDate: null,
        contractEndDate: null
      }
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  async created() {
    await this.getDepartmentsFilter()
    await this.fetchData()
    this.$nextTick(() => {
      this.$refs.tree.setCurrentKey(1)
      this.currentFilterDepartmentKey = 1
    })
  },
  methods: {
    async fetchData(params = {}, search = false) {
      try {
        this.listLoading = true
        if (!search) {
          this.isSearch = false
          params.departmentId = this.currentFilterDepartmentKey
        } else {
          this.isSearch = true
          this.currentFilterDepartmentKey = null
        }
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
        this.currentFilterDepartmentKey = data.id
        await this.fetchData()
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
          if (this.showMoveForm) {
            try {
              await employeeMove(this.employeeMoveForm)
              Message({
                message: '操作成功',
                type: 'success',
                duration: '2000'
              })
              this.showMoveForm = false
              this.resetForm(formName)
              this.employeeMoveForm.employeeId = null
              this.fetchData()
            } catch (error) {
              return
            }
          }
          if (this.renewDialog) {
            try {
              const submitObj = {
                employeeId: this.renewForm.employeeId,
                contractBeginDate: this.renewForm.contractBeginDate,
                contractEndDate: this.renewForm.contractEndDate
              }
              await employeeRenew(submitObj)
              Message({
                message: '续约成功',
                type: 'success',
                duration: '2000'
              })
              this.renewForm.employeeId = null
              this.renewForm.beforeContractBeginDate = null
              this.renewForm.beforeContractEndDate = null
              this.resetForm(formName)
              this.renewDialog = false
              this.fetchData()
            } catch (error) {
              return
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
    handleShowChangeForm({ id }) {
      this.showChangeForm = true
      this.transferForm.employeeId = id
    },
    search() {
      if (this.checkQuery()) {
        const queryObj = {}
        Object.keys(this.query).forEach(key => {
          if (this.query[key]) {
            queryObj[key] = this.query[key]
          }
        })
        this.fetchData(queryObj, true)
      } else {
        this.fetchData(null, true)
      }
    },
    checkQuery() {
      if (this.query.id || this.query.jobId || this.query.type) {
        return true
      } else {
        return false
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
    handleEmployeeMove({ id }) {
      this.showMoveForm = true
      this.employeeMoveForm.employeeId = id
    },
    geToDetailView({ id }) {
      this.$router.push({
        path: `/personnel-information/detail/${id}`
      })
    },
    handleShowRenew(row) {
      this.renewDialog = true
      this.renewForm.beforeContractBeginDate = row.contractBeginDate
      this.renewForm.beforeContractEndDate = row.contractEndDate
      this.renewForm.employeeId = row.id
    },
    closeRenewDialog() {
      this.renewForm.employeeId = null
      this.renewForm.beforeContractBeginDate = null
      this.renewForm.beforeContractEndDate = null
      this.resetForm('renewForm')
    },
    isAdmin() {
      if (this.roles.includes('admin')) {
        return true
      } else {
        return false
      }
    },
    handleDelete({ id }) {
      this.$confirm('确认删除吗', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        await deleteEmployee({ id: id })
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

<style lang="scss" scoped>

</style>
