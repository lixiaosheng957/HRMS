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
