import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
import userRouter from '@/router/module/user'
import employeeRouter from '@/router/module/employee'
import traningRouter from '@/router/module/traning'
import operateLogRouter from '@/router/module/operateLog'
import settingRouter from '@/router/module/setting'
/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '??????', icon: 'dashboard' }
    }]
  }
]

export const asyncRoutes = [
  userRouter,
  employeeRouter,
  traningRouter,
  {
    path: '/organization',
    component: Layout,
    redirect: '/organization/department',
    meta: {
      icon: 'organization',
      title: '??????',
      roles: ['admin', 'hr']
    },
    children: [
      {
        path: 'department',
        component: () => import('@/views/organization/department'),
        name: 'Department',
        meta: {
          icon: 'user',
          title: '????????????',
          roles: ['admin']
        }
      },
      {
        path: 'rank',
        component: () => import('@/views/organization/rank'),
        name: 'Rank',
        meta: {
          icon: 'user',
          title: '??????',
          roles: ['admin', 'hr']
        }
      }
    ]
  },
  operateLogRouter,
  settingRouter,
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
