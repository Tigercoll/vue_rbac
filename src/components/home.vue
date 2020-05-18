<template>
  <el-container class="full-height">
    <!-- 头部 -->
    <el-header>
      头部logo<el-button
        type="info"
        @click="logout"
      >
        退出登录
      </el-button>
    </el-header>
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="collapse ? '64px':'200px'">
        <div
          class="toggle-button"
          @click="toggle_aside"
        >
          |||
        </div>
        <!-- 菜单区域 -->
        <el-menu
          background-color="#D3DCE6"
          unique-opened
          router
          :collapse="collapse"
          :collapse-transition="false"
          :default-active="active_url"
          @select="onSelect"
        >
          <el-submenu
            v-for="(menu, index) in menus_list"
            :key="menu.id"
            :index="String(index)"
          >
            <!-- 一级菜单的模板区域 -->
            <template slot="title">
              <!-- 一级菜单的图标 -->
              <i class="el-icon-location" />
              <!-- 一级菜单的文字 -->
              <span>{{ menu.authName }}</span>
            </template>
            <!-- 二级菜单 -->
            <el-menu-item
              v-for="second_menu in menu.children"
              :key="second_menu.id"
              :index="second_menu.path"
            >
              <template slot="title">
                <!-- 二级菜单的图标 -->
                <i class="el-icon-menu" />
                <!-- 二级菜单的文字 -->
                <span @click="get_menu_name(menu.authName,second_menu.authName)">{{ second_menu.authName }}</span>
              </template>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <!-- 主体部分 -->
      <el-main>
        <el-breadcrumb separator-class="el-icon-arrow-right">
          <el-breadcrumb-item :to="{ path: 'home' }">
            首页
          </el-breadcrumb-item>
          <el-breadcrumb-item v-cloak>
            {{ second_name }}
          </el-breadcrumb-item>
          <el-breadcrumb-item v-cloak>
            {{ third_name }}
          </el-breadcrumb-item>
        </el-breadcrumb>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data () {
    return {
      menus_list: [],
      collapse: false,
      active_url: '',
      second_name: '用户管理',
      third_name: '用户列表'

    }
  },
  created () {
    this.get_menus_list()
  },
  methods: {
    logout () {
      // 清空token
      window.sessionStorage.clear()
      // 跳转到login
      this.$router.push('login')
    },
    async get_menus_list () {
      var result = await this.$http.get('menus')
      if (result.data.meta.status !== 200) {
        return this.$message({
          showClose: true,
          message: result.data.meta.msg,
          type: 'error'
        })
      }
      this.menus_list = result.data.data
    },
    toggle_aside () {
      this.collapse = !this.collapse
    },
    onSelect (index) {
      this.active_url = index
    },
    get_menu_name (secondName, thirdName) {
      this.second_name = secondName
      this.third_name = thirdName
    }
  }

}
</script>

<style lang="less" scoped>
.full-height{
  height: 100%;
}
.el-header{
  display: flex;
  background-color: #B3C0D1;
  justify-content: space-between;
  padding: 10px;
  }
.el-aside{
  background-color: #D3DCE6;
  }
.el-main{
  background-color: #E9EEF3;
}
.toggle-button{
  background-color: #69a8fb;
  text-align: center;
  cursor: pointer;
  user-select:none;
}
</style>
