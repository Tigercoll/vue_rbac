<template>
  <div>
    <el-card class="box-card">
      <!-- <el-table :data="rights_list" style="width: 80%" border stripe>
        <el-table-column type="index" label="#" />
        <el-table-column prop="authName" label="权限名称" />
        <el-table-column prop="path" label="权限路径" />
        <el-table-column prop="level" label="权限等级">
          <el-tag v-if="scope.row.level==0" slot-scope="scope">一级权限</el-tag>
          <el-tag v-else-if="scope.row.level==1" slot-scope="scope" type="success">二级权限</el-tag>
          <el-tag v-else type="danger">三级权限</el-tag>
        </el-table-column>
      </el-table> -->
      <!-- <el-row :gutter="20">
        <el-col :span="6">
          <el-button
            type="primary"

          >
            添加权限
          </el-button>
        </el-col>
      </el-row> -->
      <TreeTable
        class="tabcs"
        :data="rights_list"
        :columns="columns"
        show-index
        index-text="#"
        :expand-type="false"
        :selection-type="false"
      >
        <!-- 等级模板 -->
        <template
          slot="showLevel"
          slot-scope="scope"
        >
          <el-tag v-if="scope.row.level===0">
            一级权限
          </el-tag>
          <el-tag
            v-else-if="scope.row.level===1"
            type="success"
          >
            二级权限
          </el-tag>
          <el-tag
            v-else
            type="danger"
          >
            三级权限
          </el-tag>
        </template>
        <!-- 操作模板 -->
        <!-- <template slot="opt">
            <el-button type="primary" icon="el-icon-edit" size="small">编辑</el-button>
            <el-button type="danger" icon="el-icon-delete" size="small">删除</el-button>
        </template> -->
      </TreeTable>
    </el-card>
  </div>
</template>
<script>
export default {
  data () {
    return {
      rights_list: [],
      columns: [
        {
          label: '权限名称',
          prop: 'authName'
        },
        {
          label: '权限路径',
          prop: 'path'
        },
        {
          label: '权限等级',
          prop: 'level',
          type: 'template',
          template: 'showLevel'
        }
        //   {
        //       label: '操作',
        //     type: 'template',
        //     template: 'opt',
        //   }

      ]
    }
  },
  created () {
    this.get_rights_list()
  },
  methods: {
    async get_rights_list () {
      const { data: result } = await this.$http.get('rights/tree')
      this.rights_list = result.data
    }
  }
}
</script>

<style lang="less" scoped>
.tabcs{
    margin-top: 20px;
}
</style>
