import request from '@/utils/request'

export function getDepartments(parms) {
  return request({
    url: '/department/get-department-list',
    method: 'get',
    params: { ...parms }
  })
}
