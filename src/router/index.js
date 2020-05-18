import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/login.vue'
import Register from '../components/register.vue'
import Home from '../components/home.vue'
import Welcome from '../components/welcome.vue'
import User from '../components/users/user.vue'
import Role from '../components/roles/role.vue'
import Right from '../components/rights/right.vue'
Vue.use(VueRouter)
const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  {
    path: '/home',
    component: Home,
    redirect: '/welcome',
    children: [
      { path: '/welcome', component: Welcome },
      { path: '/users', component: User },
      { path: '/roles', component: Role },
      { path: '/rights', component: Right }
    ]
  }
]
const router = new VueRouter({
  routes
})

// 挂在路由导航守卫
router.beforeEach((to, from, next) => {
  // to 将要访问的路劲
  // form 代表从哪个路径跳转过来
  // next 是一个函数表示放行
  // next()放行 next(/login)强制跳转
  // to and from are Route Object,next() must be called to resolve the hook}
  if (to.path === '/login' || to.path === '/register') {
    return next()
  }
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) {
    return next('/login')
  }
  next()
})

export default router
