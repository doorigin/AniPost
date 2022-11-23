<template>
    <div class="container">
        <h5 class="my-3 border-bottom pb-2">질문 등록</h5>
        <form action="/" class="my-3">
            <div class="mb-3">
                <label for="subject">제목</label>
                <input v-model="subject" type="text" class="form-control">
            </div>
            <div class="mb-3">
                <label for="content">내용</label>
                <ckeditor :editor="editor" v-model="editorData" :config="editorConfig"></ckeditor>
            </div>
            <a @click="UpdatePost" href="/" class="btn btn-primary">저장하기</a>
        </form>
    </div>
</template>

<script>
import axios from 'axios'
import ClassicEditor from '@ckeditor/ckeditor5-build-classic'

export default {
    name: 'MakePost',
    data() {
        return {
            subject: null,
            editor: ClassicEditor,
            editorData: '<p>Hello</p>',
            editorConfig: {
                // The configuration of the editor.
            }
        }
    },
    async created() {
        var PrevPost = await axios.get('http://127.0.0.1:8000/api/posts' + '?id=' + this.$route.params.id)
        this.subject = PrevPost.data.subject
        this.editorData = PrevPost.data.content
    },
    methods: {
        UpdatePost() {
            let token = localStorage.getItem('access_token')
            axios({
                method: 'put',
                url: 'http://127.0.0.1:8000/api/posts' + '?id=' + this.$route.params.id,
                data: JSON.stringify({
                    "subject": this.subject,
                    "content": this.editorData
                }),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': `bearer ${token}`
                }
            })
        }
    },
}
</script>

<style>

</style>