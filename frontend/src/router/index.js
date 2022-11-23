import { createWebHistory, createRouter} from 'vue-router';
import MakePost from '../views/MakePost.vue';
import UpdatePost from '../views/UpdatePost.vue';
import PostDetail from '../views/PostDetail.vue';
import home from '../views/home.vue'
import LogIn from '../views/LogIn.vue'
import SignUp from '../views/SignUp.vue'

const routes = [
    {
        path: "/",
        name: 'Home',
        component: home
    },
    {
        path: "/login",
        name: 'Login',
        component: LogIn
    },
    {
        path: "/signup",
        name: 'SignUp',
        component: SignUp
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