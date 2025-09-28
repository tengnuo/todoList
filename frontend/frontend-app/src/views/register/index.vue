<template>
    <div>
        <h2>用户注册</h2>
        <el-form :model="userForm" :rules="rules" ref="userForm" label-width="100px" class="user-register">
            <el-form-item label="用户名" prop="username">
                <el-input v-model="userForm.username"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
                <el-input type="password" @input="checkPswStrength" v-model="userForm.password" autocomplete="off"></el-input>
                <span :class="strengthClass">密码强度: {{ pswStrength }}</span>
                <el-progress 
                    :percentage="strengthScore" 
                    :status="strengthStatus" 
                    style="margin-top: 2px;"
                    :stroke-width="8">
                </el-progress>
            </el-form-item>
            <el-form-item label="确认密码" prop="checkPass">
                <el-input type="password" v-model="userForm.checkPass" autocomplete="off"></el-input>
            </el-form-item>
            
            <el-form-item>
                <el-button type="primary" :loading="loading" @click="submitForm('userForm')">立即创建</el-button>
                <el-button @click="resetForm('userForm')">重置</el-button>
                <el-button @click="toLogin">去登录</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import request from '@/utils/request';

export default {
    name :'RegisterIndex',
    data() {
        return {
            userForm: {
                username:'',
                password:'',
                checkPass:''
            },
            rules: {
                username: [
                    { required: true, trigger: 'blur', message: '请输入用户名' },
                   
                ],
                password: [
                    { required: true, trigger: 'blur', message: '请输入密码' },
                    {   pattern: /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z]{8,16}$/, 
                        message: '密码必须包含数字和字母，长度在8-16之间', 
                        trigger: 'blur'
                    },
                    
                ],
                checkPass: [
                {   validator:(rule, value, callback) => {
                      if (value === '') {
                        callback(new Error('请再次输入密码'));
                      } 
                      else if (value !== this.userForm.password) {
                          callback(new Error('两次输入密码不一致'));
                      }
                      else {
                        callback()
                      } 
                    }}
                ]
            },
            pswStrength: '',
            strengthClass:'',
            strengthStatus:'',
            strengthScore: 0,
        }
    },
    methods: {
        submitForm(userForm) {
            this.loading = true
            this.$refs[userForm].validate( async (valid)=>{
                if (valid){
                    try{
                        const res = await request.post('/user/register', this.userForm)
                        this.$message.success(res.data.message)
                        this.$router.replace('/user/login')
                        this.$refs[userForm].resetFields()
                    } catch (err){
                        const errMsg = err.response.data.error
                        if (errMsg === '用户名已存在'){
                            const usernameField = this.$refs[userForm].fields.find(field => field.prop === 'username');
                            if (usernameField) { // 先判断字段是否存在
                                usernameField.validateMessage = errMsg; // 直接赋值，无可选链
                                usernameField.validateState = 'error';
                            }
                        }else {
                            // 2. 其他错误
                            this.$message.error(errMsg);
                        }
                    }
                }
            })
            this.loading = false
        },
        resetForm(userForm) {
            this.$refs[userForm].resetFields();
        },
        toLogin(){
            this.$router.replace('/user/login')
        },
        checkPswStrength(){
            const psw = this.userForm.password
            let score = 0
            if (psw.length >= 8){
                score += 15
            }
            if (psw.match(/[0-9]/)){
                score += 15
            }
            if (psw.match(/[a-z]/)){
                score += 20
            }
            if (psw.match(/[A-Z]/)){
                score += 20
            }
            if (psw.match(/[^0-9a-zA-Z]/)){
                score += 30
            }
            if (score <= 30){ 
                this.pswStrength = '弱'
                this.strengthClass = 'weak'
                this.strengthStatus = 'exception'
            }
            else if (score <= 40){ 
                this.pswStrength = '中'
                this.strengthClass = 'medium'
                this.strengthStatus = 'warning'
            }
            else { 
                this.pswStrength = '强'
                this.strengthClass = 'strong'
                this.strengthStatus = 'success'
            }
            this.strengthScore = score
        }
    }
}
</script>

<style scoped>
.weak{
    color: red;
}
.medium{
    color: orange;
}
.strong{
    color: green;
}
</style>