<template>
    <div>
      <h2>登录</h2>
      <input v-model="username" placeholder="用户名" />
      <input v-model="password" type="password" placeholder="密码" />
      <button @click="login">登录</button>
      <p>没有账号？<router-link to="/user/register">去注册</router-link></p>
    </div>
  </template>
  
  <script>
  import request from "@/utils/request";
  
  export default {
    name: 'LoginIndex',
    data() {
      return {
        username: "",
        password: ""
      };
    },
    methods: {
      async login() {
        try {
          const res = await request.post("/user/login", {
            username: this.username,
            password: this.password
          });
          this.$store.commit('user/setUserInfo', { token: res.data.token } )
          this.$router.replace("/tasks");
        } catch (err) {
          const errMsg = err.response.data.error
          alert(errMsg);
        }
      }
    }
  };
  </script>
  