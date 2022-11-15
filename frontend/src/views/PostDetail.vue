<template>
    <div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{{post.subject}}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text">
                {{post.content}}
            </div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">작성 시각</div>
                    <div>{{post.create_date}}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"> 
                    추천
                    <span class="badge rounded-pill bg-success">1</span>
                </button>
                <router-link :to="`/post/modify/${this.$route.params.id}`" class="btn btn-sm btn-outline-secondary">수정</router-link>
                <a href="/" @click="DeletePost" class="btn btn-sm btn-outline-secondary">삭제</a>
            </div>
        </div>
    </div>

    <h3 class="border-bottom py-2">{{comments.length}}개의 댓글</h3>

    <!-- 답변 목록 -->
    <div v-for="comment in comments" :key="comment" class="card my-3">
        <div class="card-body">
            <div class="card-text">
                {{comment.content}}
            </div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">답변자 이름</div>
                    <div>답변등록시각</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"> 
                    추천
                    <span class="badge rounded-pill bg-success">추천수</span>
                </button>
                <a class="btn btn-sm btn-outline-secondary">수정</a>
                <button @click="DeleteComment(comment.id)" class="btn btn-sm btn-outline-secondary">삭제</button>
            </div>
        </div>
    </div>
    <!-- 답변 등록 -->
    <form v-on:submit="CreateComment" class="my-3">
        <div class="mb-3">
            <textarea v-model="new_comment" rows="5" class="form-control" />
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary" />
    </form>
</div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
        post: { 
            // 이게 먼저 생기고 api 정보로 바뀌는 버그가 있음
            subject: "아직",
            content: '마다',
            create_time: 0
        },
        comments: {},
        new_comment: null
    }
  },
  async beforeCreate() {
    await axios
      .get('http://127.0.0.1:8000/api/posts' + '?id=' + this.$route.params.id)
      .then(response => (this.post = response.data))
    await axios
      .get('http://127.0.0.1:8000/api/posts/comments' + '?id=' + this.$route.params.id)
      .then(response => (this.comments = response.data))
  },
  methods: {
    DeletePost() {
        let token = localStorage.getItem('access_token')
        console.log(token)
        axios.delete('http://127.0.0.1:8000/api/posts' + '?id=' + this.$route.params.id, {
            headers: {
                'accept': 'application/json',
                'Authorization': `bearer ${token}`
            }
        })
    },
    CreateComment() {
        let token = localStorage.getItem('access_token')
        axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/api/posts/comments' + '?id=' + this.$route.params.id,
            data: JSON.stringify({
                "content": this.new_comment
            }),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `bearer ${token}`
            }
        })
    },
    DeleteComment(id) {
        let token = localStorage.getItem('access_token')
        axios.delete(`http://127.0.0.1:8000/api/post/delete_comment/${id}`, {
            headers: {
                'Authorization': `bearer ${token}`
            }
        })
        this.$router.go(0);
    }
  },
  components: {
  }
}
</script>

<style>

</style>