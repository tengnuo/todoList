import Vue from "vue"
import VueRouter from "vue-router"
import Router from "vue-router"
import Home from "@/views/layout/home.vue"
import User from "@/views/layout/user.vue"
import Layout from "@/views/layout"

Vue.use(Router)

const router = new VueRouter({
    mode: "history",
    routes: [
        {
            path: '/',
            component: Layout,
            redirect: "home",
            children: [
                { path: "home", component: Home},
                { path: 'user', component: User}
            ]
        },
        {
            path: "/login",
            component: ()=>import("@/views/login/index.vue")
        }
    ]
})

export default router