<template>
  <div class="login-container">
    <div class="login-box">
      <!-- 头像区域 -->
      <div class="avatar">
        <img
          src="../assets/tiger.jpg"
          alt
        >
      </div>
      <!-- 表单区域 -->
      <el-form
        ref="registerRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="80px"
        class="login-form"
      >
        <!-- 用户名 -->
        <el-form-item
          prop="username"
          label="用户名"
        >
          <el-input v-model="registerForm.username" />
        </el-form-item>
        <!-- 密码 -->
        <el-form-item
          label="密 码"
          prop="password"
        >
          <el-input
            v-model="registerForm.password"
            type="password"
            show-password
          />
        </el-form-item>
        <el-form-item
          label="确认密码"
          prop="password_2"
        >
          <el-input
            v-model="registerForm.password_2"
            type="password"
            show-password
          />
        </el-form-item>
        <el-form-item
          label="邮 箱"
          prop="email"
        >
          <el-input v-model="registerForm.email" />
        </el-form-item>
        <el-form-item
          label="手 机"
          prop="mobile"
        >
          <el-input v-model="registerForm.mobile" />
        </el-form-item>
        <!-- 按钮区域 -->
        <el-form-item class="btns">
          <el-button
            type="primary"
            @click="registerValid"
          >
            注册
          </el-button>
          <el-button
            type="info"
            @click="resetRegisterForm"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.registerForm.password_2 !== '') {
          this.$refs.registerRef.validateField('password_2')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.registerForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    //    验证邮箱的
    var checkEmail = (rule, value, callback) => {
      // 验证邮箱的正则表达式
      const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/

      if (regEmail.test(value)) {
        // 合法的邮箱
        return callback()
      }

      callback(new Error('请输入正确的邮箱'))
    }
    // 验证手机号的规则
    var checkMobile = (rule, value, callback) => {
      // 验证手机号的正则表达式
      const regMobile = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/

      if (regMobile.test(value)) {
        return callback()
      }

      callback(new Error('请输入正确的手机号'))
    }
    return {
      registerForm: {
        username: '',
        password: '',
        password_2: '',
        email: '',
        mobile: ''
      },
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { required: true, min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { validator: validatePass, trigger: 'blur' },
          { required: true, min: 6, max: 20, message: '长度在 3 到 20个字符', trigger: 'blur' }

        ],
        password_2: [
          { validator: validatePass2, trigger: 'blur' },
          { required: true, min: 6, max: 20, message: '长度在 3 到 20个字符', trigger: 'blur' }
        ],
        email: [
          { message: '请输入邮箱', trigger: 'blur' },
          { validator: checkEmail, trigger: 'blur' }

        ],
        mobile: [
          { message: '请输入手机', trigger: 'blur' },
          { validator: checkMobile, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    registerValid () {
      // 在提交前再次确认表单内容是否正确
      this.$refs.registerRef.validate(async valid => {
        if (!valid) { return }
        try {
          var { data: result } = await this.$http.post('register', this.$qs.stringify(this.registerForm))
          if (result.meta.status !== 201) {
            return this.$message.error(result.meta.msg)
          }
          this.$message.success(result.meta.msg)
          this.$router.push('login')
        } catch (eMsg) {
          this.$message.error(eMsg.message)
        }
      })
    },
    resetRegisterForm () {
      this.$refs.registerRef.resetFields()
    }
  }
}
</script>
<style lang="less" scoped>
.login-container {
  height: 100%;
  background: url(../assets/p1.jpg) no-repeat;
  background-size: 100%;
  }
.login-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width:600px;
  height: 500px;
  border-radius: 3px;
  opacity: 0.93;
  background-color: rgb(5, 0, 0);
}
.avatar {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 130px;
  height: 130px;
  background-color: #fff;
  border-radius: 50%;
  box-shadow: 0 0 10px #ccc;
  border: 1px solid #eee;
  padding: 10px;

  img {
    height: 100%;
    width: 100%;
    border-radius: 50%;
    background-color: #ccc;
  }
}
.btns {
  display: flex;
  justify-content: flex-end;
}
.login-form {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0 10px;
  box-sizing: border-box;
}
.el-input__inner{
    width: 90%;
}
</style>
