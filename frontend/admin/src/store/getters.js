const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  id: state => state.user.id,
  roles: state => state.user.roles,
  lastLoginTime: state => state.user.lastLoginTime,
  lastLoginIp: state => state.user.lastLoginIp,
  currentLoginIp: state => state.user.currentLoginIp,
  permission_routes: state => state.permission.routes,
  avatar: state => state.user.avatar
}
export default getters
