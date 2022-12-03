<template>
    <div class="container my-3">
    <!-- 질문 -->
    <h3 class="border-bottom py-2">내 정보</h3>
    <p v-for="item in $store.state.userInfo" :key="item">{{item}}</p>

    <h3 class="border-bottom py-2">내가 쓴 글</h3>
    <p v-for="item in mypostlist" :key="item">{{item}}</p>
    </div>
</template>


<script>
import axios from 'axios';
import { mapState } from "vuex";

export default {
  name: 'App',
  data() {
    return {
        mypostlist: {}
    }
  },
  async beforeMount() {
    axios({
        method: 'get',
        url: 'user/me/items'
    })
    .then(response => (this.mypostlist = response.data))
  },
  methods: {

  },
  computed: {
    ...mapState(["userInfo", "isLogin", "isLoginError"])
  },
  components: {
  }
}
</script>

<style>

</style>