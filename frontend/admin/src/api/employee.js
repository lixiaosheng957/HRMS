import request from '@/utils/request'

export function getEmployeeList(params) {
  return request({
    url: '/employee/getlist',
    method: 'get',
    params: { ...params }
  })
}

export function addEmployee(data) {
  return request({
    url: '/employee/add',
    method: 'post',
    data: data
  })
}

export function getEmployee(params) {
  return request({
    url: '/employee/get-employee',
    method: 'get',
    params: { ...params }
  })
}

export function editEmployee(data) {
  return request({
    url: '/employee/modify',
    method: 'post',
    data: data
  })
}
