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
      name: 'OverTimeApplicate',
      component: () => import('@/views/attendance/overTime'),
      meta: {
        icon: 'user',
        title: '加班申请',
        roles: ['admin']
      }
    },
    {
      path: 'ask-for-leave',
      name: 'AskForLeave',
      component: () => import('@/views/attendance/askForLeave'),
      meta: {
        icon: 'user',
        title: '请假申请',
        roles: ['admin']
      }
    }
  ]
}

export default attendanceRouter
