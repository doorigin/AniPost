<template>
    <div class="container">
        <div>{{this.$store.state.token}}</div>
        <h5 class="my-3 border-bottom pb-2">질문 등록</h5>
        <div class="my-3">
            <div class="mb-3">
                <label for="subject">제목</label>
                <input v-model="subject" type="text" class="form-control">
            </div>
            <div class="mb-3">
                <label for="content">내용</label>
                <ckeditor :editor="editor" v-model="editorData" :config="editorConfig"></ckeditor>
            </div>
            <a @click="CreatePost" class="btn btn-primary">저장하기</a>
        </div>

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
            editorData: '<p>Content of the editor.</p>',
            editorConfig: {
                // The configuration of the editor.
            }
        }
    },
    components: {

        },
    methods: {
        CreatePost() {
            let token = localStorage.getItem("access_token")
            console.log(this.editorData)
            axios({
                method: 'post',
                url: 'posts',
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
    }
}
</script>

<style>
.ck-editor__editable {
    min-height: 300px
}
</style>