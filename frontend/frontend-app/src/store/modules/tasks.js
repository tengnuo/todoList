import request from '@/utils/request'
export default {
    namespaced: true,
    state() {
        return {
            tasks:[]
        }
    },
    mutations: {
        setTasks(state, tasks) {
            state.tasks = tasks
        },
        addTask(state, newTask) {
            state.tasks.push(newTask)
        },
        deleteTask(state, taskId) {
            state.tasks = state.tasks.filter(task => task.id !== taskId)
        },
        editTask(state, newTask) {
            const index = state.tasks.findIndex(task => task.id === newTask.id)
            state.tasks.splice(index, 1, newTask)
        }
    },
    getters: {},
    actions: {
        async fetchTasks(context){
            const res = await request.get('/tasks/query/all')
            context.commit('setTasks', res.data.data)
        },
        async addTask(context, newTask){
            const res = await request.post('/tasks/add', newTask)   
            context.commit('addTask', res.data.data)
        },
        async deleteTask(context, id){
            await request.delete(`/tasks/delete/${id}`)
            context.commit('deleteTask', id)
        },
        async editTask(context, newTask){
            const res = await request.put(`/tasks/update/${newTask.id}`, newTask)
            context.commit('editTask', res.data.data)
        }
    }
}