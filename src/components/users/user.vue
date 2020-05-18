<template>
  <div>
    <el-card class="box-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="queryUserinfo.query"
            placeholder="请输入内容"
            clearable
            @clear="getUserList"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getUserList"
            />
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-button
            type="primary"
            @click="addUserDialogVisible=true"
          >
            添加用户
          </el-button>
        </el-col>
      </el-row>
      <!-- 用户列表区域 -->
      <el-table
        :data="userList"
        style="width: 100%"
        border
        stripe
      >
        <el-table-column type="index" />
        <el-table-column
          prop="username"
          label="姓名"
          width="180"
        />
        <el-table-column
          prop="email"
          label="邮箱"
          width="180"
        />
        <el-table-column
          prop="mobile"
          label="电话"
        />
        <el-table-column
          prop="role_name"
          label="角色"
        />
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-tooltip
              effect="dark"
              content="修改"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                circle
                @click="editUserinfo(scope.row.id)"
              />
            </el-tooltip>
            <el-tooltip
              effect="dark"
              content="删除"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                circle
                @click="removeUserinfo(scope.row.id)"
              />
            </el-tooltip>
            <el-tooltip
              effect="dark"
              content="分配角色"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="warning"
                icon="el-icon-setting"
                circle
                @click="assignRoles(scope.row)"
              />
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页区域 -->
      <el-pagination
        class="middle"
        :current-page="queryUserinfo.pagenum"
        :page-sizes="[1, 2, 5, 10]"
        :page-size="queryUserinfo.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
      <!-- 添加用户对话框 -->
      <el-dialog
        title="添加用户"
        :visible.sync="addUserDialogVisible"
        width="50%"
        @close="addFormRset"
      >
        <!-- 主体部分 -->
        <el-form
          ref="addFormRef"
          :model="addForm"
          :rules="addFormRules"
          label-width="70px"
        >
          <el-form-item
            label="用户名"
            prop="username"
          >
            <el-input v-model="addForm.username" />
          </el-form-item>
          <el-form-item
            label="密码"
            prop="password"
          >
            <el-input
              v-model="addForm.password"
              type="password"
            />
          </el-form-item>
          <el-form-item
            label="邮箱"
            prop="email"
          >
            <el-input v-model="addForm.email" />
          </el-form-item>
          <el-form-item
            label="手机"
            prop="mobile"
          >
            <el-input v-model="addForm.mobile" />
          </el-form-item>
        </el-form>
        <!-- 对话框的底部按钮 -->
        <span
          slot="footer"
          class="dialog-footer"
        >
          <el-button @click="addUserDialogVisible = false">取 消</el-button>
          <el-button
            type="primary"
            @click="addUser"
          >确 定</el-button>
        </span>
      </el-dialog>
      <!-- 修改用户信息对话框 -->
      <el-dialog
        title="修改用户信息"
        :visible.sync="editUserDialogVisible"
        width="50%"
        @close="EditFromRest"
      >
        <!-- 主体部分 -->
        <el-form
          ref="editUserFormRef"
          :model="editUserForm"
          :rules="addFormRules"
          label-width="70px"
        >
          <el-form-item label="用户名">
            <el-input
              v-model="editUserForm.username"
              disabled
            />
          </el-form-item>
          <el-form-item
            label="邮箱"
            prop="email"
          >
            <el-input v-model="editUserForm.email" />
          </el-form-item>
          <el-form-item
            label="手机"
            prop="mobile"
          >
            <el-input v-model="editUserForm.mobile" />
          </el-form-item>
        </el-form>
        <!-- 对话框的底部按钮 -->
        <span
          slot="footer"
          class="dialog-footer"
        >
          <el-button @click="editUserDialogVisible = false">取 消</el-button>
          <el-button
            type="primary"
            @click="editUser"
          >确 定</el-button>
        </span>
      </el-dialog>
      <!-- 分配角色对话框 -->
      <el-dialog
        title="分配角色"
        :visible.sync="rolesDialogVisible"
        width="50%"
        @close="clearTab"
      >
        <!-- 主体部分 -->
        <el-form
          :model="rolesForm"
          label-width="80px"
        >
          <el-form-item label="用户名:">
            <span v-text="rolesForm.username" />
          </el-form-item>
          <el-form-item label="当前角色:">
            <span v-text="rolesForm.currentRole" />
          </el-form-item>
          <el-form-item label="新的角色:">
            <el-select
              v-model="value"
              placeholder="请选择"
            >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
        </el-form>
        <!-- 对话框的底部按钮 -->
        <span
          slot="footer"
          class="dialog-footer"
        >
          <el-button @click="rolesDialogVisible = false">取 消</el-button>
          <el-button
            type="primary"
            @click="setRoles"
          >确 定</el-button>
        </span>
      </el-dialog>
    </el-card>
  </div>
</template>
<script>
export default {
  data () {
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

      queryUserinfo: {
        query: '',
        // 当前页码数
        pagenum: 1,
        // 当前每页显示多少条数据
        pagesize: 10
      },
      userList: [],
      total: 0,
      addUserDialogVisible: false,
      addForm: {
        username: '',
        password: '',
        email: '',
        mobile: ''
      },
      addFormRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { validator: checkEmail, trigger: 'blur' }

        ],
        mobile: [
          { required: true, message: '请输入手机', trigger: 'blur' },
          { validator: checkMobile, trigger: 'blur' }
        ]
      },
      editUserDialogVisible: false,
      editUserForm: {},
      rolesForm: {
        id: '',
        username: '',
        currentRole: '',
        newRole: ''
      },
      rolesDialogVisible: false,
      // 下拉菜单
      options: [],
      value: ''
    }
  },
  created () {
    this.getUserList()
  },
  methods: {
    //   获取用户信息
    async getUserList () {
      var result = await this.$http.get('users', {
        params: this.queryUserinfo
      })
      if (result.data.meta.status !== 200) {
        return this.$message.error(result.data.meta.msg)
      }
      this.userList = result.data.data.users
      this.total = result.data.data.totalpage
    },
    // 监听页码数改变事件
    handleSizeChange (newSize) {
      this.queryUserinfo.pagesize = newSize
      this.getUserList()
    },
    // 监听页数改变时间
    handleCurrentChange (newPage) {
      this.queryUserinfo.pagenum = newPage
      this.getUserList()
    },
    // 监听用户更改状态
    async changeUserState (userinfo) {
      const { data: result } = await this.$http.put(
        `users/${userinfo.id}/state/${userinfo.mg_state}`
      )
      if (result.meta.status !== 200) {
        userinfo.mg_state = !userinfo.mg_state
        return this.$message.error(result.meta.msg)
      }
      this.$message.success(result.meta.msg)
    },
    // 关闭对话框清空表单内容
    addFormRset () {
      this.$refs.addFormRef.resetFields()
    },
    // 添加用户
    addUser () {
      // 添加用户前需要再次验证表单
      this.$refs.addFormRef.validate(async valid => {
        if (!valid) {
          return
        }
        //    通过后发起添加请求

        const { data: result } = await this.$http.post('users', this.$qs.stringify(this.addForm))
        if (result.meta.status !== 201) {
          return this.$message.error(result.meta.msg)
        }
        this.$message.success(result.meta.msg)
        this.addUserDialogVisible = false
        this.getUserList()
      })
    },
    // 点击修改,打开编辑按钮,并通过ID 向后台获取数据
    async editUserinfo (id) {
      const { data: result } = await this.$http.get('users/' + id)
      if (result.meta.status !== 200) {
        return this.$message.error(result.meta.msg)
      }
      this.editUserForm = result.data
      this.editUserDialogVisible = true
    },
    // 重置修改页面的验证信息
    EditFromRest () {
      this.$refs.editUserFormRef.resetFields()
    },
    editUser () {
      this.$refs.editUserFormRef.validate(async valid => {
        if (!valid) { return }
        const { data: result } = await this.$http.put('users/' + this.editUserForm.id, this.$qs.stringify({
          email: this.editUserForm.email,
          mobile: this.editUserForm.mobile
        }))
        if (result.meta.status !== 200) {
          this.$message.error(result.meta.msg)
        }
        this.$message.success(result.meta.msg)
        this.getUserList()
        this.editUserDialogVisible = false
      })
    },
    // 打开删除消息提示
    removeUserinfo (id) {
      // 询问用户是否删除
      this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'error'
      }).then(async () => {
        const { data: result } = await this.$http.delete('users/' + id)
        if (result.meta.status === 200) {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.getUserList()
        } else {
          this.$message({
            type: 'error',
            message: '删除出错!'
          })
        }
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 打开分配角色对话框
    async assignRoles (userinfo) {
      this.rolesForm.id = userinfo.id
      this.rolesForm.username = userinfo.username
      this.rolesForm.currentRole = userinfo.role_name
      const { data: result } = await this.$http.get('roles')
      if (result.meta.status !== 200) {
        return this.$message.error(result.meta.msg)
      }
      result.data.forEach(element => {
        this.options.push({
          value: String(element.id),
          label: String(element.roleName)
        })
      })
      this.rolesDialogVisible = true
    },
    // 清空下拉菜单
    clearTab () {
      this.options = []
      this.value = ''
    },
    // 点击确定上传roles
    async setRoles () {
      if (!this.value) {
        this.$alert('你还没有选择新的角色', '提示', {
          confirmButtonText: '确定'
        })
        return
      }
      const { data: result } = await this.$http.put(`users/${this.rolesForm.id}/role`, this.$qs.stringify({ rid: this.value }))
      if (result.meta.status !== 200) {
        this.$message.error(result.meta.msg)
      }
      this.$message.success(result.meta.msg)
      this.clearTab()
      this.getUserList()
      this.rolesDialogVisible = false
    }
  }

}
</script>

<style lang="less" scoped>
.el-breadcrumb {
  margin-bottom: 15px;
}
.el-table {
  margin-top: 15px;
}
.el-pagination {
  margin-top: 15px;
}
.middle{
 display: flex;
 justify-content:flex-end;
}
</style>
