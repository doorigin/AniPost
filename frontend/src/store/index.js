import router from '@/router'
import axios from 'axios'
import { createStore } from 'vuex'

export default createStore({
  state: {
    userInfo: "로그인 전",
    isLogin: false,
    isLoginError: false
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
    logout(state) {
      state.isLogin = false
      state.isLoginError = false
    }
  },
  actions: {
    async login({commit}, loginObj) {
      await axios
        .post("user/token", loginObj, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        })
        .then(
          await commit('loginSuccess')
        )
        .catch((error) => {
          console.log(error)
          commit('loginError')
        })
        // dispatch('getUserInfo')
      // this.$router.push("/")
      },
    async getUserInfo({ commit }) {
      let config = {
        withCredentials: true,
      }
      await axios
        .get("user/me", config)
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
          console.log('이메일과 비밀번호를 확인하세요1')
        })
      },
    logout({ commit }) {
      document.cookie = "access_token" + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;'
      commit("logout")
      router.push({ name: "Home" })
    }
  },
  modules: {
  }
})
