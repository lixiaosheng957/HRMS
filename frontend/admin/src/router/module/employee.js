import Layout from '@/layout'

const employeeRouter = {
  path: '/personnel-information',
  component: Layout,
  redirect: '/personnel-information/employee',
  meta: {
    icon: 'user',
    title: '人员信息',
    roles: ['admin']
  },
  children: [
    {
      path: 'employee',
      component: () => import('@/views/personnelInformation/employee'),
      name: 'Employee',
      meta: {
        icon: 'user',
        title: '员工管理',
        roles: ['admin']
      }
    },
    {
      path: 'resign',
      component: () => import('@/views/personnelInformation/resign'),
      name: 'ResignEmployee',
      meta: {
        icon: 'user',
        title: '离职员工',
        roles: ['admin']
      }
    },
    {
      path: 'change',
      component: () => import('@/views/personnelInformation/change'),
      name: 'ChangeEmployee',
      meta: {
        icon: 'user',
        title: '变动记录',
        roles: ['admin']
      }
    }
  ]
}

export default employeeRouter
