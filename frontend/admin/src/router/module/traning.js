import Layout from '@/layout'

const traningRouter = {
  path: '/training',
  component: Layout,
  meta: {
    icon: 'user',
    title: '培训',
    roles: ['admin']
  },
  children: [
    {
      path: 'project',
      name: 'TrainingProject',
      component: () => import('@/views/training/project'),
      meta: {
        icon: 'user',
        title: '培训计划',
        roles: ['admin']
      }
    },
    {
      path: 'trainers',
      name: 'Trainers',
      component: () => import('@/views/training/trainers'),
      meta: {
        icon: 'user',
        title: '培训人员',
        roles: ['admin']
      }
    }
  ]
}

export default traningRouter
