import Layout from '@/layout'

const traningRouter = {
  path: '/training',
  component: Layout,
  meta: {
    icon: 'training',
    title: '培训',
    roles: ['admin', 'hr']
  },
  children: [
    {
      path: 'project',
      name: 'TrainingProject',
      component: () => import('@/views/training/project'),
      meta: {
        icon: 'training',
        title: '培训计划',
        roles: ['admin', 'hr']
      }
    },
    {
      path: 'program_assess',
      name: 'ProgramAssess',
      component: () => import('@/views/training/trainingAssess'),
      meta: {
        icon: 'assess',
        title: '培训评价',
        roles: ['admin', 'hr']
      }
    },
    {
      path: 'assess/:id',
      name: 'Assess',
      component: () => import('@/views/training/assess'),
      hidden: true,
      meta: {
        title: '评价',
        roles: ['admin', 'hr']
      }
    }
  ]
}

export default traningRouter
