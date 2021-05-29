import request from '@/utils/request'

export function getJobList(parms) {
  return request({
    url: '/api/job-level/get-job-level-list',
    method: 'get',
    params: { ...parms }
  })
}

export function addJob(data) {
  return request({
    url: '/api/job-level/add',
    method: 'post',
    data: data
  })
}

export function deleteJob(data) {
  return request({
    url: '/api/job-level/delete',
    method: 'post',
    data: data
  })
}
