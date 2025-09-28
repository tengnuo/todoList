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
        }
    },
    getters: {},
    actions: {
        async fetchTasks(context){
            const res = await request.get('/tasks/query/all')
            context.commit('setTasks', res.data.data)
        }
    }
}