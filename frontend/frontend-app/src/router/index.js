import Vue from "vue"
import VueRouter from "vue-router"
import Router from "vue-router"
import Task from "@/views/layout/task.vue"
import User from "@/views/layout/user.vue"
import Layout from "@/views/layout"

Vue.use(Router)

const router = new VueRouter({
    mode: "history",
    routes: [
        {
          path: '/',
          component: Layout,
          redirect: "/tasks",
          children: [
              { path: "/tasks", component: Task,  meta: { requiresAuth: true }},
              { path: '/user/profile', component: User}
          ]
        },
        {
          path: "/user/login",
          component: ()=>import("@/views/login/index.vue")
        },
        {
          path: '/user/register',
          component: ()=>import('@/views/register/index.vue')
        }
    ]
})

// 路由守卫：没有 token 不能访问任务页
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token");
    if (to.meta.requiresAuth && !token) {
      next("/user/login");
    } else {
      next();
    }
  });

export default router