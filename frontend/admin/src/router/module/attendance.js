import Layout from '@/layout'

const attendanceRouter = {
  path: '/attendance',
  component: Layout,
  meta: {
    icon: 'user',
    title: '假勤',
    roles: ['admin']
  },
  children: [
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
      name: 'OverTimeApplicate',
      component: () => import('@/views/attendance/overTime'),
      meta: {
        icon: 'user',
        title: '加班审批',
        roles: ['admin']
      }
    },
    {
      path: 'ask-for-leave',
      name: 'AskForLeave',
      component: () => import('@/views/attendance/askForLeave'),
      meta: {
        icon: 'user',
        title: '请假审批',
        roles: ['admin']
      }
    }
  ]
}

export default attendanceRouter
