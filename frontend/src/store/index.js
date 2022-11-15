import router from '@/router'
import axios from 'axios'
import { createStore } from 'vuex'

export default createStore({
  state: {
    userInfo: "로그인 전",
    isLogin: false,
    isLoginError: false,
    token: null
  },
  getters: {
  },
  mutations: {
    // 로그인 성공 시
    loginSuccess(state, payload) {
      console.log('Login Success!!')
      state.isLogin = true
      state.isLoginError = false
      state.userInfo = payload
    },
    // 로그인 실패 시
    loginError(state) {
      state.isLogin = false
      state.isLoginError = true
    },
    setToken(state, payload) {
      state.token = payload
    }
  },
  actions: {
    login({ dispatch, commit }, loginObj) {
      axios
        .post("http://127.0.0.1:8000/api/user/token", loginObj, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        })
        .then(res => {
          // 성공 시 토큰을 받아 옴. 이걸 헤더에 포함시켜 유저 정보
          let token = res.data.access_token
          localStorage.setItem("access_token", token)
          dispatch('getUserInfo')
          commit('setToken', token)
        })
        .catch(() => {
          alert('이메일과 비밀번호를 확인하세요')
        })
      },
    getUserInfo({ commit }) {
      let token = localStorage.getItem("access_token")
      let config = {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      }
      axios
        .get("http://127.0.0.1:8000/api/user/me", config)
        .then(response => {
          console.log(response.data)
          let userInfo = {
            id: response.data.id,
            username: response.data.username,
            email: response.data.email,
            full_name: response.data.full_name,
            disabled: response.data.disabled
          }
          commit('loginSuccess', userInfo)
        })
        .catch(() => {
          alert('이메일과 비밀번호를 확인하세요1')
        })
      },
    logout({ commit }) {
      commit("logout")
      router.push({ name: "home" })
    }
  },
  modules: {
  }
})
