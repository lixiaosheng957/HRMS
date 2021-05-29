import request from '@/utils/request'

export function statisticsForEmployeeType(params) {
  return request({
    url: '/api/statistics/employee-type-statistics',
    method: 'get',
    params: { ...params }
  })
}

export function statisticsForDepartmentEmployeeCount(params) {
  return request({
    url: '/api/statistics/department-employee-statistics',
    method: 'get',
    params: { ...params }
  })
}

export function statisticsPersonnelInfo(params) {
  return request({
    url: '/api/statistics/personnel-info-statistics',
    method: 'get',
    params: { ...params }
  })
}

export function getToBeRenewList(params) {
  return request({
    url: '/api/statistics/to-be-renew',
    method: 'get',
    params: { ...params }
  })
}

export function getContractEndList(params) {
  return request({
    url: '/api/statistics/contract-end',
    method: 'get',
    params: { ...params }
  })
}

export function getUndoneTrainingProgramList(params) {
  return request({
    url: '/api/statistics/undone-training-program',
    method: 'get',
    params: { ...params }
  })
}
