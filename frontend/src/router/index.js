import { createWebHistory, createRouter} from 'vue-router';
import MakePost from '../views/MakePost.vue';
import UpdatePost from '../views/UpdatePost.vue';
import PostDetail from '../views/PostDetail.vue';
import home from '../views/home.vue'

const routes = [
    {
        path: "/",
        name: 'Home',
        component: home
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
        path: "/post/view/:id",
        name: 'PostDetail',
        component: PostDetail
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router