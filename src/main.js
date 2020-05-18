import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
// 配置全局样式
import './assets/css/global.css'
// 配置字体图标
import './assets/font/iconfont.css'
import { MessageBox, Message } from 'element-ui'
// 导入tree-grid
import TreeTable from 'vue-table-with-tree-grid'

// 导入axios
import axios from 'axios'
import qs from 'qs'
// 导入qs
// 配置请求根路径
axios.defaults.baseURL = 'http://127.0.0.1:3000/api/private/v1/'
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-fromurlencodeed'
// 配置请求拦截器
axios.interceptors.request.use(config => {
  config.headers.Authorization = window.sessionStorage.getItem('token')
  return config
})
axios.interceptors.response.use(config => {
  if (config.data.meta && config.data.meta.status === 401) {
    Message.alert('登录超时,请重新登录!', '登录超时', {
      confirmButtonText: '跳转至登录页面',
      callback: action => {
        router.push('login')
      }
    })
  }
  return config
})
Vue.prototype.$http = axios
Vue.prototype.$qs = qs
Vue.config.productionTip = false
Vue.component('TreeTable', TreeTable)
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
