<template>
    <div class="container my-3">
    <div class="row my-3">
        <div class="col-6">
            <router-link to="/post/create" class="btn btn-primary">질문 등록하기</router-link>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" v-model="searchkeyword" @keypress.enter="SearchKeyword">
                <button @click="SearchKeyword" class="btn btn-outline-secondary">찾기</button>
            </div>
        </div>
    </div>
    <table class="table">
        <thead>
        <tr class="text-center table-dark">
            <th>번호</th>
            <th style="width:50%">제목</th>
            <th>글쓴이</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(a, i) in postdata" :key="i" class="text-center">
            <td>{{postdata[i].id}}</td>
            <td>
                <router-link :to="`/post/view/${postdata[i].id}`">{{postdata[i].subject}}</router-link>
            </td>
            <td>작성자1</td>
            <td>{{postdata[i].create_date}}</td>
        </tr>
        
        </tbody>
    </table>

    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
        postdata: null,
        searchkeyword: null
    }
  },
  async created() {
    await axios
      .get('http://127.0.0.1:8000/api/post/list')
      .then(response => (this.postdata = response.data))
  },
  methods: { //method가 아니고 query param으로 해결할것 (?search=제목2)
    SearchKeyword() {
      if(this.searchkeyword == ("" | null)) {
        axios
        .get('http://127.0.0.1:8000/api/post/list')
        .then(response => (this.postdata = response.data))
      } else {
      axios
      .get('http://127.0.0.1:8000/api/post/search/'+this.searchkeyword)
      .then(response => (this.postdata = response.data))
    }}
  }
}
</script>

<style>
</style>
