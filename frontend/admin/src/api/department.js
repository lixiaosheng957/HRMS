import request from '@/utils/request'

export function getDepartments(parms) {
  return request({
    url: '/department/get-department-list',
    method: 'get',
    params: { ...parms }
  })
}

export function addDepartment(data) {
  return request({
    url: '/department/add',
    method: 'post',
    data: data
  })
}

export function deleteDepartment(data) {
  return request({
    url: '/department/delete',
    method: 'post',
    data: data
  })
}

export function getDepartment(params) {
  return request({
    url: '/department/get',
    method: 'get',
    params
  })
}

export function editDepartment(data) {
  return request({
    url: '/department/modify',
    method: 'post',
    data: data
  })
}
