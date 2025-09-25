<template>
    <div>
        <el-row><el-button type="primary" round @click="showAddDialog = true">添加任务</el-button></el-row>
        <el-table
            :data="tasks.filter(task => !search || task.title.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%; margin-top: 20px">
            <el-table-column label="标题" prop="title"></el-table-column>
            <el-table-column label="描述" prop="description"></el-table-column>
            <el-table-column label="优先级" prop="priority"></el-table-column>
            <el-table-column label="截止日期" prop="due_date"></el-table-column>
            <el-table-column label="完成状态">
                <template slot-scope="scope">
                    <el-checkbox v-model="scope.row.completed" @change="toggleComplete(scope.row)"></el-checkbox>
                </template>
            </el-table-column>
            <el-table-column align="right">
                <!-- 表头搜索框 -->
                <template slot="header">
                <el-input
                    v-model="search"
                    size="mini"
                    placeholder="输入关键字搜索"
                />
                </template>

                <!-- 行操作 -->
                <template slot-scope="scope">
                <el-button size="mini" @click="editTask(scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="deleteTask(scope.row.id)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import request from '@/utils/request'

export default{
    name: 'TaskIndex',
    data(){
        return {
            tasks:[],
            search:''
        }
    },
    created() {
        this.getTasks()
    },
    methods: {
        async getTasks(){
            const res = await request.get('/tasks/query/all')
            this.tasks = res.data.data
        }
        
    }
}
</script>