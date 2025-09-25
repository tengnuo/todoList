import axios from 'axios'
import store from '../store'

const request = axios.create({
  baseURL: 'http://127.0.0.1:5000', // 服务器地址P
  timeout: 5000,
})

// 请求拦截器：只要有token，就在请求时携带便于请求需要授权的接口
request.interceptors.request.use(config => {
  const token = store.getters['user/token']
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
}, function (error) {
  // 对请求错误做些什么
  return Promise.reject(error)
})

export default request
