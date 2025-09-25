<template>
    <div>
        <el-row><el-button type="primary" round @click="centerDialogVisible = true">添加任务</el-button></el-row>
        <el-table
            :data="tasks.filter(task => !search || task.title.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%; margin-top: 20px">
            <el-table-column label="标题" prop="title"></el-table-column>
            <el-table-column label="描述" prop="description"></el-table-column>
            <el-table-column label="优先级" prop="priority"></el-table-column>
            <el-table-column label="截止日期" prop="due_date"></el-table-column>
            <el-table-column label="完成状态">
                <template>
                    <el-checkbox>已完成</el-checkbox>
                </template>
            </el-table-column>
            <el-table-column
                align="right">
                <template slot="header">
                    <el-input
                    v-model="search"
                    size="mini"
                    placeholder="输入关键字搜索"/>
                </template>
                <template slot-scope="scope">
                    <el-button
                    size="mini"
                    @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button
                    size="mini"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-dialog destroy-on-close :visible.sync="centerDialogVisible" title="添加任务" width="500" center draggable>
            <el-form :inline="true" :model="newTask" :rules="rules" label-width="120px">
                <el-form-item label="任务名称" prop="title">
                    <el-input v-model="newTask.title" placeholder="请输入新任务"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input v-model="newTask.description"></el-input>
                </el-form-item>
                <el-form-item label="优先级">
                    <el-dropdown @command="handlePriority">
                        <span class="el-dropdown-link">
                            {{ newTask.priority || '请选择优先级' }}<i class="el-icon-arrow-down el-icon--right"></i>
                        </span>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item command="高">高</el-dropdown-item>
                            <el-dropdown-item command="中">中</el-dropdown-item>
                            <el-dropdown-item command="低">低</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </el-form-item>
                <el-form-item label="截止日期">
                    <el-date-picker
                        v-model="newTask.due_date"
                        type="date"
                        placeholder="选择日期"
                        value-format="yyyy-MM-dd"
                    />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="centerDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="addTask">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import request from '@/utils/request'

export default{
    name: 'TaskIndex',
    data(){
        return {
            tasks:[],
            search:'',
            centerDialogVisible: false,  // 控制弹窗显示
            newTask: {             // 表单数据
                title: '',
                description: '',
                priority: '',
                due_date: ''
            },
            rules : {
                title: [
                    { required: true, message: '请输入任务名称', trigger: 'blur' }
                ]
            }
        }
    },
    created() {
        this.getTasks()
    },
    methods: {
        async getTasks(){
            const res = await request.get('/tasks/query/all')
            this.tasks = res.data.data
        },
        async addTask() {
            if (this.newTask.title == ''){
                alert('任务名称不能为空')
                return 
            }
            await request.post('/tasks/add', this.newTask)
            this.getTasks()
            this.centerDialogVisible = false
        },
        handlePriority(value) {
            this.newTask.priority = value
        }
        
    },
}
</script>

<style scoped>
  .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
</style>