import request from '@/utils/request'

export function getEmployeeList(params) {
  return request({
    url: '/api/employee/getlist',
    method: 'get',
    params: { ...params }
  })
}

export function addEmployee(data) {
  return request({
    url: '/api/employee/add',
    method: 'post',
    data: data
  })
}

export function getEmployee(params) {
  return request({
    url: '/api/employee/get-employee',
    method: 'get',
    params: { ...params }
  })
}

export function editEmployee(data) {
  return request({
    url: '/api/employee/modify',
    method: 'post',
    data: data
  })
}

export function transfer(data) {
  return request({
    url: '/api/employee/transfer',
    method: 'post',
    data: data
  })
}

export function getTransferRecordsList(params) {
  return request({
    url: '/api/employee/get-transfer-records',
    method: 'get',
    params: { ...params }
  })
}

export function getTransferDetail(params) {
  return request({
    url: '/api/employee/get-transfer-detail',
    method: 'get',
    params: { ...params }
  })
}

export function employeeMove(data) {
  return request({
    url: '/api/employee/move',
    method: 'post',
    data: data
  })
}

export function getEmployeeMoveList(params) {
  return request({
    url: '/api/employee/get-employee-move-list',
    method: 'get',
    params: { ...params }
  })
}

export function getEmployeeMoveDetail(params) {
  return request({
    url: '/api/employee/get-employee-move-detail',
    method: 'get',
    params: { ...params }
  })
}

export function employeeRenew(data) {
  return request({
    url: '/api/employee/renew',
    method: 'post',
    data: data
  })
}

export function deleteEmployee(data) {
  return request({
    url: '/api/employee/delete',
    method: 'post',
    data: data
  })
}
