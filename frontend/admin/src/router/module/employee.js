import Layout from '@/layout'

const employeeRouter = {
  path: '/personnel-information',
  component: Layout,
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
        title: '正式员工',
        roles: ['admin']
      }
    },
    {
      path: 'tryout',
      component: () => import('@/views/personnelInformation/tryout'),
      name: 'TryoutEmployee',
      meta: {
        icon: 'user',
        title: '试用员工',
        roles: ['admin']
      }
    },
    {
      path: 'practice',
      component: () => import('@/views/personnelInformation/practice'),
      name: 'PracticeEmployee',
      meta: {
        icon: 'user',
        title: '实习员工',
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
        title: '员工变动',
        roles: ['admin']
      }
    }
  ]
}

export default employeeRouter
