import request from '@/utils/request'

export function statisticsForEmployeeType(params) {
  return request({
    url: '/statistics/employee-type-statistics',
    method: 'get',
    params: { ...params }
  })
}

export function statisticsForDepartmentEmployeeCount(params) {
  return request({
    url: '/statistics/department-employee-statistics',
    method: 'get',
    params: { ...params }
  })
}

export function statisticsPersonnelInfo(params) {
  return request({
    url: '/statistics/personnel-info-statistics',
    method: 'get',
    params: { ...params }
  })
}

export function getToBeRenewList(params) {
  return request({
    url: '/statistics/to-be-renew',
    method: 'get',
    params: { ...params }
  })
}

export function getContractEndList(params) {
  return request({
    url: '/statistics/contract-end',
    method: 'get',
    params: { ...params }
  })
}

export function getUndoneTrainingProgramList(params) {
  return request({
    url: '/statistics/undone-training-program',
    method: 'get',
    params: { ...params }
  })
}
