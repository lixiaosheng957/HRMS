import request from '@/utils/request'

export function getJobList(parms) {
  return request({
    url: 'job-level/get-job-level-list',
    method: 'get',
    params: { ...parms }
  })
}

export function addJob(data) {
  return request({
    url: '/job-level/add',
    method: 'post',
    data: data
  })
}
