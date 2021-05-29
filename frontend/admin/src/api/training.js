import request from '@/utils/request'

export function addTrainingProgram(data) {
  return request({
    url: '/api/training/add-training-program',
    method: 'post',
    data: data
  })
}

export function deleteTrainingProgram(data) {
  return request({
    url: '/api/training/delete-training-program',
    method: 'post',
    data: data
  })
}

export function getTrainingProgramList(params) {
  return request({
    url: '/api/training/get-program-list',
    method: 'get',
    params: { ...params }
  })
}

export function getTrainingProgramDetail(params) {
  return request({
    url: '/api/training/get-program-detail',
    method: 'get',
    params: { ...params }
  })
}

export function searchTrainingProgram(params) {
  return request({
    url: '/api/training/get-program-list',
    method: 'get',
    params: { ...params }
  })
}

export function publishProgram(data) {
  return request({
    url: '/api/training/publish',
    method: 'post',
    data: data
  })
}

export function editProgramBaseInfo(data) {
  return request({
    url: '/api/training/modify-program-base',
    method: 'post',
    data: data
  })
}

export function editProgramParticipant(data) {
  return request({
    url: '/api/training/modify-training-people',
    method: 'post',
    data: data
  })
}

export function getUnfinishAssessProgramList(params) {
  return request({
    url: '/api/training/get-undone-access-program-list',
    method: 'get',
    params
  })
}

export function getUndoneAccessPeople(params) {
  return request({
    url: '/api/training/get-undone-access-people',
    method: 'get',
    params
  })
}

export function assess(data) {
  return request({
    url: '/api/training/assess',
    method: 'post',
    data: data
  })
}

export function getunFinishProgramDoneAssessList(params) {
  return request({
    url: '/api/training/get-undone-assess-program-done-assess-people-list',
    method: 'get',
    params
  })
}

export function getFinishAssProgramList(params) {
  return request({
    url: '/api/training/get-done-assess-program-list',
    method: 'get',
    params
  })
}

export function getFinishAssProgramDetail(params) {
  return request({
    url: '/api/training/get-done-assess-program-detail',
    method: 'get',
    params
  })
}
