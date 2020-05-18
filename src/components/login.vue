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
        ref="loginRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="0px"
        class="login-form"
      >
        <!-- 用户名 -->
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            prefix-icon="iconfont icon-yonghu"
          />
        </el-form-item>
        <!-- 密码 -->
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            prefix-icon="iconfont icon-mima"
            type="password"
          />
        </el-form-item>
        <!-- 按钮区域 -->
        <el-form-item class="btns">
          <el-button
            type="primary"
            @click="loginValid"
          >
            登录
          </el-button>
          <el-button
            type="success"
            @click="registerBtn"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      // 校验规则,通过rules属性
      loginRules: {
        // 用户名校验规则
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        // 密码校验规则
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 跳转到注册页
    registerBtn () {
      this.$router.push('register')
    },
    // 提交前验证表单合法性
    loginValid () {
      this.$refs.loginRef.validate(async valid => {
        // 如果不合法直接返回
        if (!valid) {
          return
        }
        try {
          var result = await this.$http.post('login', this.$qs.stringify(this.loginForm))

          if (result.data.meta.status !== 200) {
            return this.$message({
              showClose: true,
              message: result.data.meta.msg,
              type: 'error'
            })
          } else {
          // 登录成功后的操作
          // 1,将登录成功之后的token,保存到客户端的sessionStorage中
          // 1.1项目中除了登录之外的其他API接口,必须在登录之后才能访问
          // 1.2 token只应在当前网站打开期间生效,所以将token保存在sessionStorage 而不是local Storage中
          // 2,通过编程式导航跳转到后台主页,路由为/home
            this.$message({
              showClose: true,
              message: result.data.meta.msg,
              type: 'success'
            })
            window.sessionStorage.setItem('token', result.data.data.token)
            this.$router.push('/home')
          }
        } catch (err) {
          this.$message({
            showClose: true,
            message: err.message,
            type: 'error'
          })
        }
      })
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
  width: 450px;
  height: 300px;
  border-radius: 3px;
  opacity: 0.9;
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
</style>
