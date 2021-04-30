import Layout from '@/layout'

const operateLogRouter = {
  path: '/operate-log',
  component: Layout,
  meta: {
    icon: 'record',
    title: '操作记录',
    roles: ['admin', 'hr']
  },
  children: [
    {
      path: 'mine',
      name: 'OperateLogRecord',
      component: () => import('@/views/operateLog/index'),
      meta: {
        icon: 'record',
        title: '我的操作记录',
        roles: ['admin', 'hr']
      }
    },
    {
      path: 'all',
      name: 'AllOperateLogRecord',
      component: () => import('@/views/operateLog/All'),
      meta: {
        icon: 'record',
        title: '全部操作记录',
        roles: ['admin']
      }
    }
  ]
}

export default operateLogRouter
