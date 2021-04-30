<template>
  <div class="app-container">
    <el-header>
      <el-row>
        <el-col :span="4">
          <h3>修改密码</h3>
        </el-col>
      </el-row>
      <el-main>
        <el-form>
          <el-row>
            <el-col :span="6">
              <el-form-item label="账号" label-width="90px">
                <el-input v-model="username" type="text" :disabled="true" placeholder="请输入密码" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="5">
            <el-col :span="6">
              <el-form-item label="密码" label-width="90px">
                <el-input v-model="password" :type="passwordType" placeholder="请输入密码" />
                <span class="show-pwd" @click="showPwd">
                  <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
                </span>
              </el-form-item>
            </el-col>
            <el-col :span="1">
              <el-button type="primary" @click="handleUpdate">更新</el-button>
            </el-col>
          </el-row>
        </el-form>
      </el-main>
    </el-header>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { Message } from 'element-ui'
import { changePasswordForSelf } from '@/api/user'
const checkPassword = (value) => {
  if (!value) {
    return {
      current: false,
      msg: '请输入密码'
    }
  } else if (value.length < 6) {
    return {
      current: false,
      msg: '密码长度过短'
    }
  } else {
    return {
      current: true,
      msg: '格式正确'
    }
  }
}
export default {
  name: 'ChangePassWord',
  data() {
    return {
      password: '',
      passwordType: 'password'
    }
  },
  computed: {
    ...mapGetters([
      'username'
    ])
  },
  created() {

  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    async handleUpdate() {
      const valid = checkPassword(this.password)
      if (valid.current) {
        try {
          await changePasswordForSelf({
            password: this.password
          })
          Message({
            message: '修改成功',
            type: 'success',
            duration: 2000
          })
          this.password = ''
        } catch (error) {
          return
        }
      } else {
        Message({
          message: valid.msg,
          type: 'warning',
          duration: 2000
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
$dark_gray:#889aa4;
.show-pwd {
    position: absolute;
    right: 10px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
</style>
