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
                        <p>用户名：{{ userInfo.username }}</p>
                        <p>年龄：{{ getAge }}</p>
                        <p>性别：{{ userInfo.gender || '未设置'}}</p>
                        <div class="hobby">
                            <ul>
                                <li v-for="(item, index) in userInfo.hobby" :key="index">{{ item }}</li>
                            </ul>
                        </div>
                    </div>
                    <div class="btn">
                        <el-button icon="el-icon-edit" type="text" round @click="handleEdit">修改信息</el-button>
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

        <!-- 编辑个人信息弹出框 -->
        <el-dialog destroy-on-close :visible.sync="centerDialogVisible" title="编辑信息" width="500" center draggable>
            <el-form :inline="true" :model="newInfo" ref="infoForm" :rules="rules" label-width="120px">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="newInfo.username" placeholder="请输入用户名"></el-input>
                </el-form-item>
                <el-form-item label="性别">
                    <el-select v-model="newInfo.gender" placeholder="请选择性别">
                        <el-option label="男" value="男" />
                        <el-option label="女" value="女" />
                        <el-option label="其他" value="其他" />
                    </el-select>
                </el-form-item>
                <el-form-item label="出生日期">
                    <el-date-picker
                        v-model="newInfo.birth_date"
                        type="date"
                        placeholder="选择日期"
                        value-format="yyyy-MM-dd"
                        :picker-options="optionsDisable"
                    />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="centerDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="submitForm()">提交</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import request from '@/utils/request'

export default{
    name: 'UserIndex',
    data() {
        return {
            userInfo: {
                id: null,
                username: '',
                avatarURL:'',
                gender: '',
                birth_date: '',
                hobby: ['吃饭', '睡觉', '打游戏']
            },
            isProfileLoaded: false, // 标记用户信息是否加载完成
            centerDialogVisible: false,
            newInfo: {  // 表单数据
                username: '',
                gender: '',
                birth_date: ''
            },
            optionsDisable: {
                disabledDate(time) {
                    return time.getTime() > Date.now()
                }
            },
        }
    },
    created(){
        this.$store.dispatch('tasks/fetchTasks')
        this.getUserInfo()
    },
    methods: {
        async getUserInfo() {
            const res = await request.get('/user/profile')
            this.userInfo = res.data.data
            this.isProfileLoaded = true
        },
        async submitForm() {
            try{
                const res = await request.put('/user/update', {
                    username: this.newInfo.username,
                    gender: this.newInfo.gender,
                    birth_date: this.newInfo.birth_date
                })
                this.$message.success(res.data.msg)
                this.centerDialogVisible = false
                // 更新用户信息
                this.userInfo = { ...this.userInfo, ...this.newInfo }
                this.userInfo.age = this.getAge()
                // 重置表单
                this.$refs.infoForm.resetFields()
            }catch(err){
                const errMsg = err.response.data.msg
                this.$message.error(errMsg)
            }finally{
                this.centerDialogVisible = false
            }
            
        },
        handleEdit() {
            Object.assign(this.newInfo, this.userInfo) // 将用户信息复制到表单中
            this.centerDialogVisible = true
        }
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
        },
        getAge() {
            if (!this.isProfileLoaded) return null
            const birthDate = this.userInfo.birth_date
            if (!birthDate) return null
            
            // 解析出生日期和当前日期
            const birth = new Date(birthDate.replace(/-/g, "/"))            
            const now = new Date()
            
            // 计算年份差
            let age = now.getFullYear() - birth.getFullYear()
            
            // 对比月份：若当前月份 < 出生月份，年龄减 1
            if (now.getMonth() < birth.getMonth()) {
                age--
            } 
            // 月份相同但日期 < 出生日期，年龄减 1
            else if (now.getMonth() === birth.getMonth() && now.getDate() < birth.getDate()) {
                age--
            }
            return age
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