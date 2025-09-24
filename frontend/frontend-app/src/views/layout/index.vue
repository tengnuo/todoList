<template>
    <div>
        <h2>TodoList</h2>
        <router-view></router-view>
        <el-tabs v-model="activeName" @tab-click="handleClick" tab-position="bottom" class="bottom-tabs">
            <el-tab-pane label="首页" name="home"></el-tab-pane>
            <el-tab-pane label="用户管理" name="user"></el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
export default {
    name: 'LayoutIndex',
    data() {
      return {
        activeName: 'home'
      };
    },
    methods: {
        handleClick(tab) {
            if (this.$route.path !== `/${tab.name}`) {
                this.$router.push({ path: `/${tab.name}` })
            }
        }
    }
}

</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.bottom-tabs {
  position: fixed;    /* 固定在屏幕底部 */
  bottom: 0;
  left: 0;
  width: 100%;
}
/* 深层选择器覆盖组件自带样式 */
.bottom-tabs >>> .el-tabs__header {
  display: flex;
  justify-content: space-around; 
}
.el-tabs__item {
  flex: 1; 
  text-align: center;
}

</style>