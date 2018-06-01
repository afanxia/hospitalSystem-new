import api from '@/utils/api'

export function login(username, password) {
  return api({
    url: '/auth/login',
    method: 'post',
    data: {
      'username': username,
      'password': password
    }
  })
}

export function getInfo(token) {
  return api({
    url: '/auth/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return api({
    url: '/auth/logout',
    method: 'post'
  })
}
