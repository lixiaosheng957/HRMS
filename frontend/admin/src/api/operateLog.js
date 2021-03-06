import request from '@/utils/request'

export function getMyOperateLog(params) {
  return request({
    url: '/api/operate-log/get-my-operate-log',
    method: 'get',
    params: { ...params }
  })
}

export function getAllOperateLog(params) {
  return request({
    url: '/api/operate-log/get-all-operate-log',
    method: 'get',
    params: { ...params }
  })
}
