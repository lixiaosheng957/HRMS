import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
import userRouter from '@/router/module/user'
import employeeRouter from '@/router/module/employee'
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
      meta: { title: '首页', icon: 'dashboard' }
    }]
  }
]

export const asyncRoutes = [
  userRouter,
  employeeRouter,
  {
    path: '/attendance',
    component: Layout,
    meta: {
      icon: 'user',
      title: '假勤',
      roles: ['admin']
    },
    children: [
      {
        path: 'record',
        name: 'AttendanceRecord',
        component: () => import('@/views/attendance/record'),
        meta: {
          icon: 'user',
          title: '考勤记录',
          roles: ['admin']
        }
      },
      {
        path: 'total',
        name: 'AttendanceTotal',
        component: () => import('@/views/attendance/total'),
        meta: {
          icon: 'user',
          title: '考勤汇总',
          roles: ['admin']
        }
      },
      {
        path: 'overtime-applicate',
        name: 'AttendanceTotal',
        component: () => import('@/views/attendance/total'),
        meta: {
          icon: 'user',
          title: '加班申请',
          roles: ['admin']
        }
      },
      {
        path: 'ask-for-leave',
        name: 'AttendanceTotal',
        component: () => import('@/views/attendance/total'),
        meta: {
          icon: 'user',
          title: '请假申请',
          roles: ['admin']
        }
      }
    ]
  },
  {
    path: '/training',
    component: Layout,
    meta: {
      icon: 'user',
      title: '培训',
      roles: ['admin']
    },
    children: [
      {
        path: 'project',
        name: 'TrainingProject',
        component: () => import('@/views/training/project'),
        meta: {
          icon: 'user',
          title: '培训计划',
          roles: ['admin']
        }
      },
      {
        path: 'trainers',
        name: 'Trainers',
        component: () => import('@/views/training/trainers'),
        meta: {
          icon: 'user',
          title: '培训人员',
          roles: ['admin']
        }
      }
    ]
  },
  {
    path: '/recruitment',
    component: Layout,
    meta: {
      icon: 'user',
      title: '招聘',
      roles: ['admin']
    },
    children: [
      {
        path: '/campus',
        component: () => import('@/views/recruitment/campusRecruitment'),
        name: 'CampsRecruitment',
        meta: {
          icon: 'user',
          title: '校园招聘',
          roles: ['admin']
        }
      },
      {
        path: 'social',
        component: () => import('@/views/recruitment/recruitment'),
        name: 'SocialRecruitment',
        meta: {
          icon: 'user',
          title: '社会招聘',
          roles: ['admin']
        }
      },
      {
        path: 'to-be-hired',
        component: () => import('@/views/recruitment/recruitment'),
        name: 'SocialRecruitment',
        meta: {
          icon: 'user',
          title: '待入职',
          roles: ['admin']
        }
      }
    ]
  },
  {
    path: '/organization',
    component: Layout,
    meta: {
      icon: 'user',
      title: '组织',
      roles: ['admin']
    },
    children: [
      {
        path: 'department',
        component: () => import('@/views/organization/department'),
        name: 'Department',
        meta: {
          icon: 'user',
          title: '部门架构',
          roles: ['admin']
        }
      },
      {
        path: 'rank',
        component: () => import('@/views/organization/rank'),
        name: 'Rank',
        meta: {
          icon: 'user',
          title: '职位',
          roles: ['admin']
        }
      }
    ]
  },
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