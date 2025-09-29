<template>
    <div>
        <el-row><el-button type="primary" round @click="centerDialogVisible = true">添加任务</el-button></el-row>
        <el-table
            :data="pageTasks"
            style="width: 100%; margin-top: 20px"
            :row-class-name="tableRowClassName"
            row-key="id">
            <el-table-column 
            type="index" 
            label="序号" 
            width="100" 
            align="center"
            ></el-table-column>
            <el-table-column label="标题" prop="title"></el-table-column>
            <el-table-column label="描述" prop="description"></el-table-column>
            <el-table-column 
            label="优先级" 
            prop="priority" 
            :filters="[{ text: '高', value: '高' }, { text: '中', value: '中' }, { text: '低', value: '低' }]"
            :filter-method="filterPriority">
            </el-table-column>
            <el-table-column label="截止日期" prop="due_date" sortable></el-table-column>
            <el-table-column label="完成状态" prop="completed">
                <template #default="{row}">
                    <el-checkbox v-model="row.completed" @change="handleCompleted(row)">已完成</el-checkbox>
                </template>
            </el-table-column>
            <el-table-column
                align="right">
                <template slot="header" slot-scope="scope">
                    <!-- 显式使用 scope 变量，避免 ESLint 报错 -->
                    <div v-if="false">{{ scope }}</div>
                    <el-input
                    type="text"
                    prefix-icon="el-icon-search"
                    v-model="search"
                    size="mini"
                    placeholder="输入关键字搜索"
                    @input="handleSearch"
                    />
                </template>
                <template slot-scope="scope">
                    <el-button
                    size="mini"
                    @click="handleEdit(scope.row)">编辑</el-button>
                    <el-button
                    size="mini"
                    type="danger"
                    @click="handleDelete(scope.row.id)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- 分页 -->
        <el-row>
            <el-col :span="24" class="toolbar" style="text-align:center">
                <el-pagination
                    @current-change="handleCurrentChange"
                    layout="total, prev, pager, next"
                    :page-size="pagesize"
                    :total="sortTasks.length"
                ></el-pagination>
            </el-col>
        </el-row>
        

        <!-- 添加/编辑任务弹出框 -->
        <el-dialog destroy-on-close :visible.sync="centerDialogVisible" :title="!isEdit ? '添加任务' : '编辑任务'" width="500" center draggable>
            <el-form :inline="true" ref="taskForm" :model="newTask" :rules="rules" label-width="120px">
                <el-form-item label="任务名称" prop="title">
                    <el-input v-model="newTask.title" placeholder="请输入新任务"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input v-model="newTask.description"></el-input>
                </el-form-item>
                <el-form-item label="优先级">
                    <el-select v-model="newTask.priority" placeholder="请选择优先级">
                        <el-option label="高" value="高" />
                        <el-option label="中" value="中" />
                        <el-option label="低" value="低" />
                    </el-select>
                </el-form-item>
                <el-form-item label="截止日期">
                    <el-date-picker
                        v-model="newTask.due_date"
                        type="date"
                        placeholder="选择日期"
                        value-format="yyyy-MM-dd"
                    />
                </el-form-item>
                <el-form-item label="完成状态">
                    <el-select v-model="newTask.completed" placeholder="请选择优先级">
                        <el-option label="未完成" :value=false />
                        <el-option label="已完成" :value=true />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="centerDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="saveTask">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import request from '@/utils/request'
import { mapState } from 'vuex'

export default{
    name: 'TaskIndex',
    data(){
        return {
            search:'',
            timer: null, // 定时器
            centerDialogVisible: false,  // 控制弹窗显示
            isEdit: false,  // 判断是否是编辑模式
            editId: null,
            newTask: {             // 表单数据
                id: null,
                title: '',
                description: '',
                priority: '',
                due_date: '',
                completed: false
            },
            currentPage: 1, // 默认第一页
            pagesize: 9, //设置每页显示条目个数为10
            rules : {
                title: [
                    { required: true, message: '请输入任务名称', trigger: 'blur' }
                ]
            }
        }
    },
    created() {
        this.$store.dispatch('tasks/fetchTasks')
    },
    methods: {
        handleSearch(){
            // 添加防抖逻辑
            if (this.timer) {
                clearTimeout(this.timer)
            }
            this.timer = setTimeout(() => {
                console.log('搜索', this.search);
            }, 300)
        },
        tableRowClassName({row}) {
            // 当任务完成时，返回completed类名
            return row.completed ? 'completed' : 'uncompleted'
        },
        handleCompleted(row) {
            request.put(`/tasks/update/${row.id}`, row)  
        },
        saveTask() {
            this.$refs.taskForm.validate((valid) => {
                if (valid) {
                    // 如果是编辑模式
                    if (this.isEdit) {
                        this.$store.dispatch('tasks/editTask', this.newTask)
                    } 
                    // 如果是添加模式
                    else{
                        this.$store.dispatch('tasks/addTask', this.newTask)
                    }
                    this.centerDialogVisible = false; // 关闭弹窗
                    // 重置编辑状态
                    this.isEdit = false;
                    this.editId = null;
                    // 重置表单
                    this.$refs.taskForm.resetFields();
                }
            })

        },
        async handleDelete(id) {
            this.$store.dispatch('tasks/deleteTask', id)
        },
        async handleEdit(row) {
            this.isEdit = true
            this.editId = row.id
            Object.assign(this.newTask, row); // 将任务数据复制到表单
            this.centerDialogVisible = true
        },
        handleCurrentChange(curPage) {
            this.currentPage = curPage
        },
        filterPriority(value, row) {
            return row.priority === value
        }
    },
    computed: {
        ...mapState('tasks', ['tasks']),
        sortTasks() {
            let filteredTasks = this.tasks.filter(task => 
            !this.search || task.title.toLowerCase().includes(this.search.toLowerCase()))

            return filteredTasks.sort((a, b)=>{
                if (a.completed === b.completed) {
                    return 0
                }
                return a.completed ? 1 : -1
            })
        },
        pageTasks(){
            let start = (this.currentPage - 1) * this.pagesize
            let end = this.currentPage * this.pagesize
            return this.sortTasks.slice(start, end)
        }
    }

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
  ::v-deep .completed {
    background-color: #f5f7fa;
    text-decoration: line-through;
    color: gray;
  }

  ::v-deep .uncompleted {
    color: #000;
  }
</style>