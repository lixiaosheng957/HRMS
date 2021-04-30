import Layout from '@/layout'

const userRouter = {
  path: '/user',
  component: Layout,
  children: [
    {
      path: 'index',
      component: () => import('@/views/user'),
      name: 'Account',
      meta: {
        icon: 'account',
        title: '账号管理',
        roles: ['admin']
      }
    }
  ]
}

export default userRouter
