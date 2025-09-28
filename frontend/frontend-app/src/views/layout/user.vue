<template>
    <div>
        <h2>用户中心</h2>
        <el-row>
            <el-col :span="6" class="left">
                <el-card class="box-card">
                    <div class="avatar">
                        <img class="avatar-img" 
                        src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" alt="">
                    </div>
                    <div class="text item">
                        <p>{{ userInfo.username }}</p>
                        <span>{{ userInfo.age }}</span>
                        <span>{{ userInfo.gender }}</span>
                        <div class="hobby">
                            <ul>
                                <li v-for="(item, index) in userInfo.hobby" :key="index">{{ item }}</li>
                            </ul>
                        </div>
                    </div>
                    <div class="btn">
                        <el-button icon="el-icon-edit" type="text" round>修改信息</el-button>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="18" class="right">
                <el-card class="box-card">
                    <div slot="header" class="clearfix">
                        <span>任务详情</span>
                    </div>
                    <el-carousel :interval="4000" type="card" height="200px">
                        <el-carousel-item>
                            <h3>任务完成情况</h3> <span>完成任务/总任务</span>
                            <p>{{ stats.completedTasks }}/{{ stats.total }}</p>
                        </el-carousel-item>
                        <el-carousel-item>
                            <h3>今日任务</h3>
                            <ul>
                                <li v-for="task in stats.todayTasks" :key="task.id">
                                    {{ task.title }} ({{ task.completed ? "已完成" : "未完成" }})
                                </li>
                                <li v-if="stats.todayTasks.length === 0">今天没有任务</li>
                            </ul>
                        </el-carousel-item>
                        <el-carousel-item>
                            <h3>按时完成任务</h3>
                            <p>{{ stats.onTimeCompleted }}</p>
                        </el-carousel-item>
                        <el-carousel-item>
                            <h3>未按时完成任务</h3>
                            <p>{{ stats.unCompleted }}</p>
                        </el-carousel-item>
                    </el-carousel>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import { mapState } from 'vuex'
export default{
    name: 'UserIndex',
    data() {
        return {
            userInfo: {
                avatarURL:'',
                username: '1',
                age: '18',
                gender: '女',
                hobby: ['吃饭', '睡觉', '打游戏']
            }
        }
    },
    created(){
        this.$store.dispatch('tasks/fetchTasks')
    },
    methods: {
    },
    computed: {
        ...mapState('tasks', ['tasks']),
        stats() {
            const total = this.tasks.length
            const completedTasks = this.tasks.filter(task=>task.completed===true).length
            const date = new Date().toISOString().slice(0, 10)
            const todayTasks = this.tasks.filter(task=>task.due_date===date)
            const onTimeCompleted = this.tasks.filter(task=>
                task.completed===true && new Date(task.due_date) >= new Date(task.updated_at)
            ).length
            const unCompleted = this.tasks.filter(task=>task.completed===false).length
            return {total, completedTasks, todayTasks, onTimeCompleted, unCompleted}
        }
    }
}
</script>

<style scoped>
.avatar-img{
    border-radius: 50%;
    width: 60px;
    height: 60px;
    display: block;
    margin: 0 auto
}
.el-carousel{
    text-align: center
}
.el-carousel__item h3{
    color: #475669;
}
.el-carousel__item:nth-child(2n) {
    background-color: #FFE4E1;
}
.el-carousel__item:nth-child(2n+1) {
background-color: #FFDAB9;
}
</style>