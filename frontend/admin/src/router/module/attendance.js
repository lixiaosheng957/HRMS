import Layout from '@/layout'

const attendanceRouter = {
  path: '/attendance',
  component: Layout,
  redirect: '/attendance/overtime-applicate',
  meta: {
    icon: 'user',
    title: '假勤',
    roles: ['admin', 'hr']
  },
  children: [
    {
      path: 'overtime-applicate',
      name: 'OverTimeApplicate',
      component: () => import('@/views/attendance/overTime'),
      meta: {
        icon: 'user',
        title: '加班审批',
        roles: ['admin', 'hr']
      }
    },
    {
      path: 'ask-for-leave',
      name: 'AskForLeave',
      component: () => import('@/views/attendance/askForLeave'),
      meta: {
        icon: 'user',
        title: '请假审批',
        roles: ['admin', 'hr']
      }
    }
  ]
}

export default attendanceRouter
