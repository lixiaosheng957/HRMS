import Layout from '@/layout'

const settingRouter = {
  path: '/setting',
  component: Layout,
  meta: {
    icon: 'setting',
    title: '设置',
    roles: ['hr']
  },
  children: [
    {
      path: 'password',
      name: 'SettingPassword',
      component: () => import('@/views/setting/changePassword'),
      meta: {
        icon: 'password',
        title: '修改密码',
        roles: ['hr']
      }
    }
  ]
}

export default settingRouter

