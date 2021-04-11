import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: 'user/get-userinfo',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}

export function getUserList(currentPage, pageSize) {
  return request({
    url: 'user/list',
    method: 'get',
    params: { currentPage, pageSize }
  })
}

export function addUser(data) {
  return request({
    url: 'user/add',
    method: 'post',
    data: data
  })
}
