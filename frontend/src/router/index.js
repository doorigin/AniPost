import { createWebHistory, createRouter } from 'vue-router';
import MakePost from '../views/MakePost.vue';
import UpdatePost from '../views/UpdatePost.vue';
import PostDetail from '../views/PostDetail.vue';
import home from '../views/home.vue'
import LogIn from '../views/LogIn.vue'
import SignUp from '../views/SignUp.vue'
import UserInfo from '../views/UserInfo.vue'
import axios from 'axios'
// import store from '@/store/index.js'

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/'
axios.defaults.withCredentials = true

const routes = [
    {
        path: "/",
        name: 'Home',
        component: home
    },
    {
        path: "/login",
        name: 'Login',
        component: LogIn,
        // beforeEnter: (to, from, next) => {
        //     console.log(to, from)
        //     if(isLogin == true) {
        //         next("/")
        //     } else {
        //         next("/login")
        //     }

        // }
    },
    {
        path: "/signup",
        name: 'SignUp',
        component: SignUp
    },
    {
        path: "/userinfo",
        name: 'UserInfo',
        component: UserInfo
    },
    {
        path: "/post/create",
        name: 'MakePost',
        component: MakePost
    },
    {
        path: "/post/modify/:id",
        name: 'UpdatePost',
        component: UpdatePost
    },
    {
        path: "/post/view",
        name: 'PostDetail',
        component: PostDetail
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router