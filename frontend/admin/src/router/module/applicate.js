import Layout from '@/layout'

const appliactionRouter = {
  path: '/application',
  component: Layout,
  meta: {
    icon: 'user',
    title: '申请',
    roles: ['admin', 'employee']
  },
  children: [
    {
      path: '/applicate',
      name: 'Applicate',
      component: () => import('@/views/application/applicate'),
      meta: {
        icon: 'user',
        title: '申请提交',
        roles: ['admin', 'employee']
      }
    },
    {
      path: '/record',
      name: 'ApplicateRecord',
      component: () => import('@/views/application/applicationRecord'),
      meta: {
        icon: 'user',
        title: '申请记录',
        roles: ['admin', 'employee']
      }
    }
  ]
}

export default appliactionRouter
