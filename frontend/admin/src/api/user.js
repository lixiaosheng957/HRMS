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
    url: '/user/get-userinfo',
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

export function getUserList(params) {
  return request({
    url: '/user/list',
    method: 'get',
    params: { ...params }
  })
}

export function addUser(data) {
  return request({
    url: '/user/add',
    method: 'post',
    data: data
  })
}

export function getUserAccountTagsList(params) {
  return request({
    url: '/user/get-user-tags-list',
    method: 'get',
    params: params
  })
}

export function changePassword(data) {
  return request({
    url: '/user/modify-password',
    method: 'post',
    data: data
  })
}

export function changePasswordForSelf(data) {
  return request({
    url: '/user/change-password',
    method: 'post',
    data: data
  })
}

export function deleteAccount(data) {
  return request({
    url: '/user/delete',
    method: 'post',
    data: data
  })
}
