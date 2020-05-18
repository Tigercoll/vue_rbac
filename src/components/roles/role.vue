<template>
  <div>
    <el-card class="box-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-button
            type="primary"
            @click="dialogAddRoles = true"
          >
            添加角色
          </el-button>
        </el-col>
      </el-row>
      <el-table
        :data="rolesData"
        style="width: 100%"
        border
        stripe
      >
        <!-- 展开列 -->
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-row
              v-for="item in props.row.children"
              :key="item.id"
              :gutter="20"
              class="row-bg"
            >
              <el-col :span="5">
                <el-tag
                  closable
                  @close="removeRights(item, props.row)"
                >
                  {{
                    item.authName
                  }}
                </el-tag>
                <i class="el-icon-caret-right" />
              </el-col>
              <el-col :span="19">
                <el-row
                  v-for="item_2 in item.children"
                  :key="item_2.id"
                  class="row-bg"
                >
                  <el-col :span="6">
                    <el-tag
                      type="success"
                      closable
                      @close="removeRights(item_2, props.row)"
                    >
                      {{ item_2.authName }}
                    </el-tag>
                    <i class="el-icon-caret-right" />
                  </el-col>
                  <el-col :span="18">
                    <el-tag
                      v-for="item_3 in item_2.children"
                      :key="item_3.id"
                      type="warning"
                      closable
                      @close="removeRights(item_3, props.row)"
                    >
                      {{ item_3.authName }}
                    </el-tag>
                  </el-col>
                </el-row>
              </el-col>
            </el-row>
          </template>
        </el-table-column>
        <el-table-column
          type="index"
          label="#"
        />
        <el-table-column
          prop="roleName"
          label="角色名"
        />
        <el-table-column
          prop="roleDesc"
          label="角色描述"
        />
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-tooltip
              effect="dark"
              content="编辑"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                @click="getRolesById(scope.row)"
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
                @click="delRolesById(scope.row.id)"
              />
            </el-tooltip>
            <el-tooltip
              effect="dark"
              content="分配权限"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="warning"
                icon="el-icon-setting"
                @click="showRightsTree(scope.row)"
              />
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <!-- 添加权限对话框 -->
    <el-dialog
      title="添加角色"
      :visible.sync="dialogAddRoles"
      width="30%"
      @close="resetAddForm"
    >
      <el-form
        ref="addRolesRef"
        :model="addRolesForm"
        :rules="addRolesRules"
        label-width="80px"
      >
        <el-form-item
          label="角色名称"
          prop="rolesName"
        >
          <el-input v-model="addRolesForm.rolesName" />
        </el-form-item>
        <el-form-item
          label="角色描述"
          prop="rolesDesc"
        >
          <el-input v-model="addRolesForm.rolesDesc" />
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="dialogAddRoles = false">取 消</el-button>
        <el-button
          type="primary"
          @click="addRoles"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 编辑权限对话框 -->
    <el-dialog
      title="修改角色"
      :visible.sync="dialogEditRoles"
      width="30%"
      @close="restEditForm"
    >
      <el-form
        ref="editRolesRef"
        :model="editRolesForm"
        :rules="addRolesRules"
        label-width="80px"
      >
        <el-form-item
          label="角色名称"
          prop="rolesName"
        >
          <el-input v-model="editRolesForm.rolesName" />
        </el-form-item>
        <el-form-item
          label="角色描述"
          prop="rolesDesc"
        >
          <el-input v-model="editRolesForm.rolesDesc" />
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="dialogEditRoles = false">取 消</el-button>
        <el-button
          type="primary"
          @click="editRoles"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 分配权限对话框 -->
    <el-dialog
      title="分配权限"
      :visible.sync="dialogRolesSet"
      width="30%"
      @close="restTree"
    >
      <el-tree
        ref="rightTreeRef"
        :data="rights_data"
        :props="defaultProps"
        node-key="id"
        :default-checked-keys="checked_rigths_list"
        show-checkbox
        default-expand-all
      />
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="dialogRolesSet = false">取 消</el-button>
        <el-button
          type="primary"
          @click="allotRights"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
export default {
  data () {
    return {
      rolesData: [],
      // 打开添加角色对话框按钮
      dialogAddRoles: false,
      // 添加角色form
      addRolesForm: {
        rolesName: '',
        rolesDesc: ''
      },
      // 添加角色的规则
      addRolesRules: {
        rolesName: [
          { required: true, message: '请输入角色名称', trigger: 'blur' }
        ],
        rolesDesc: []
      },
      editRolesForm: {
        role_id: '',
        rolesName: '',
        rolesDesc: ''
      },
      dialogEditRoles: false,
      //   分配权限
      dialogRolesSet: false,
      rights_data: [],
      defaultProps: {
        id: 'id',
        children: 'children',
        label: 'authName'
      },
      checked_rigths_list: [],
      roles_id: 0
    }
  },
  created () {
    this.get_roles_list()
  },
  methods: {
    async get_roles_list () {
      var { data: result } = await this.$http.get('roles')
      if (result.meta.status !== 200) {
        this.$message.error(result.meta.msg)
      }
      this.rolesData = result.data
    },
    // 删除角色下的权限
    removeRights (rights, role) {
      const rights_name = rights.authName
      const rights_id = rights.id
      const role_id = role.id
      this.$confirm(`确定要取消${rights_name} 权限吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async () => {
          const { data: result } = await this.$http.delete(
            `roles/${role_id}/rights/${rights_id}`
          )
          if (result.meta.status !== 200) {
            throw result.meta.msg
          }
          role.children = result.data
          this.$message({
            type: 'success',
            message: '取消权限成功!'
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消权限失败'
          })
        })
    },
    // 添加角色
    addRoles () {
      this.$refs.addRolesRef.validate(async valid => {
        if (!valid) {
          return
        }
        const { data: result } = await this.$http.post(
          'roles',
          this.$qs.stringify(this.addRolesForm)
        )
        if (result.meta.status !== 201) {
          return this.$message.error(result.meta.msg)
        }
        this.$message.success(result.meta.msg)
        this.get_roles_list()
        this.dialogAddRoles = false
      })
    },
    // 重置添加表单
    resetAddForm () {
      this.$refs.addRolesRef.resetFields()
    },
    // 重置编辑表单
    restEditForm () {
      this.$refs.editRolesRef.resetFields()
    },
    // 通过id获取角色信息
    async getRolesById (roles) {
      const rid = roles.id
      const { data: result } = await this.$http.get('roles/' + rid)
      if (result.meta.status !== 200) {
        return this.$message.error(result.meta.msg)
      }
      this.editRolesForm.rolesName = result.data.roleName
      this.editRolesForm.rolesDesc = result.data.roleDesc
      this.editRolesForm.role_id = result.data.roleId
      this.dialogEditRoles = true
    },
    // 提交编辑操作
    editRoles () {
      this.$refs.editRolesRef.validate(async valid => {
        if (!valid) {
          return
        }
        const { data: result } = await this.$http.put(
          'roles/' + this.editRolesForm.role_id,
          this.$qs.stringify(this.editRolesForm)
        )
        if (result.meta.status !== 200) {
          return this.$message.error(result.meta.msg)
        }
        this.$message.success(result.meta.msg)
        this.get_roles_list()
        this.dialogEditRoles = false
      })
    },
    // 删除角色信息
    delRolesById (rid) {
      this.$confirm('是否删除该角色信息? ', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async () => {
          const { data: result } = await this.$http.delete('roles/' + rid)
          if (result.meta.status !== 200) {
            throw result.meta.msg
          }
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.get_roles_list()
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    async showRightsTree (rolesInfo) {
      this.roles_id = rolesInfo.id
      const { data: result } = await this.$http.get('rights/tree')
      if (result.meta.status !== 200) {
        return this.$message.error(result.meta.msg)
      }
      this.rights_data = result.data
      this.get_checked_rigths_id(rolesInfo, this.checked_rigths_list)
      this.dialogRolesSet = true
    },
    // 用递归的方式获取三级权限
    get_checked_rigths_id (rolesInfo, temp_list) {
      if (rolesInfo.children) {
        rolesInfo.children.forEach(element => {
          this.get_checked_rigths_id(element, temp_list)
        })
      } else {
        return temp_list.push(rolesInfo.id)
      }
    },
    // 分配权限
    async allotRights () {
      const rights_list = [
        ...this.$refs.rightTreeRef.getHalfCheckedKeys(),
        ...this.$refs.rightTreeRef.getCheckedKeys()
      ]

      const { data: result } = await this.$http.post('roles/' + this.roles_id, this.$qs.stringify({ rights_list: JSON.stringify(rights_list) }))
      if (result.meta.status !== 200) {
        return this.$message.error(result.meta.msg)
      }
      this.$message.success(result.meta.msg)
      this.get_roles_list()
      this.dialogRolesSet = false
    },
    restTree () {
      this.checked_rigths_list = []
    }
  }
}
</script>

<style lang="less" scoped>
.row-bg {
  display: flex;
  align-items: center;
}
.el-tag {
  margin: 10px;
}
</style>
