import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/api/user/get-userinfo',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/api/vue-admin-template/user/logout',
    method: 'post'
  })
}

export function getUserList(params) {
  return request({
    url: '/api/user/list',
    method: 'get',
    params: { ...params }
  })
}

export function addUser(data) {
  return request({
    url: '/api/user/add',
    method: 'post',
    data: data
  })
}

export function getUserAccountTagsList(params) {
  return request({
    url: '/api/user/get-user-tags-list',
    method: 'get',
    params: params
  })
}

export function changePassword(data) {
  return request({
    url: '/api/user/modify-password',
    method: 'post',
    data: data
  })
}

export function changePasswordForSelf(data) {
  return request({
    url: '/api/user/change-password',
    method: 'post',
    data: data
  })
}

export function deleteAccount(data) {
  return request({
    url: '/api/user/delete',
    method: 'post',
    data: data
  })
}
