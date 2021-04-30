import Layout from '@/layout'

const employeeRouter = {
  path: '/personnel-information',
  component: Layout,
  redirect: '/personnel-information/employee',
  meta: {
    icon: 'employee',
    title: '员工',
    roles: ['admin', 'hr']
  },
  children: [
    {
      path: 'employee',
      component: () => import('@/views/personnelInformation/employee'),
      name: 'Employee',
      meta: {
        icon: 'employee',
        title: '员工管理',
        roles: ['admin', 'hr']
      }
    },
    {
      path: 'detail/:id',
      component: () => import('@/views/personnelInformation/employeeDetail'),
      name: 'EmployeeDetail',
      hidden: true,
      meta: {
        title: '员工详情',
        roles: ['admin', 'hr']
      }
    },
    {
      path: 'resign',
      component: () => import('@/views/personnelInformation/resign'),
      name: 'ResignEmployee',
      meta: {
        icon: 'resign',
        title: '离职员工',
        roles: ['admin', 'hr']
      }
    },
    {
      path: 'change',
      component: () => import('@/views/personnelInformation/change'),
      name: 'ChangeEmployee',
      meta: {
        icon: 'user',
        title: '变动记录',
        roles: ['admin', 'hr']
      }
    }
  ]
}

export default employeeRouter
