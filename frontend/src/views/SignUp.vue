<template>
    <div class="container">
    <h5 class="my-3 border-bottom pb-2">회원 가입</h5>
    <form method="post">
        <div class="mb-3">
            <label for="username">아이디</label>
            <input type="text" class="form-control" id="username" v-model="username">
        </div>
        <div class="mb-3">
            <label for="username">성명</label>
            <input type="text" class="form-control" id="fullname" v-model="fullname">
        </div>
        <div class="mb-3">
            <label for="password1">비밀번호</label>
            <input type="password" class="form-control" id="password1" v-model="password1">
        </div>
        <div class="mb-3">
            <label for="password2">비밀번호 확인</label>
            <input type="password" class="form-control" id="password2" v-model="password2">
        </div>
        <div class="mb-3">
            <label for="email">이메일</label>
            <input type="text" class="form-control" id="email" v-model="email">
        </div>
        <button type="submit" class="btn btn-primary" @click="CreateUser">생성하기</button>
    </form>
</div>
</template>

<script>
import axios from 'axios';

    export default {
        name: 'SignUp',
        data() {
            return {
                username: null,
                fullname: null,
                password1: null,
                password2: null,
                email: null
            }
        },
        methods: {
            CreateUser(e) {
                e.preventDefault()
                let token = localStorage.getItem("access_token")
                axios({
                    method: 'post',
                    url: 'http://127.0.0.1:8000/api/user/create',
                    data: JSON.stringify({
                        username: this.username,
                        full_name: this.fullname,
                        password1: this.password1,
                        password2: this.password2,
                        email: this.email
                    }),
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': `bearer ${token}`
                    }
                })
            }
        }
        
    }
</script>

<style></style>