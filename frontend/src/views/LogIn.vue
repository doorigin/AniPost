<template>
    <div class="container">
        <h5 class="my-3 border-bottom pb-2">로그인</h5>
        <form action="/">
            <div class="mb-3">
                <label for="username">사용자 이름</label>
                <input type="text" class="form-control" id="username" v-model="username">
            </div>
            <div class="mb-3">
                <label for="password">비밀번호</label>
                <input type="password" class="form-control" id="password" v-model="password">
            </div>
            <button type="submit" class="btn btn-primary" @click="login({username, password})">로그인</button>
        </form>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
    name: 'LogIn',
    data() {
        return {
            username: null,
            password: null
        }
    },
    computed: {
        ...mapState(["isLogin, isLoginError"])
    },
    methods: {
        ...mapActions(["login"])
    }
}
</script>

<style></style>