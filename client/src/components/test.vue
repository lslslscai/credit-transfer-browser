<template>
  <div class="test">
    <h1>当前点击数 {{ count }}</h1>
    <el-row>
        <el-button type="primary" @click='increment'>试着点点！</el-button>
    </el-row>
    <router-link to="/">回到首页</router-link>
  </div>
</template>

<script>
export default {
  name: 'Test',
  data () {
    return {
      count: 4
    }
  },
  methods: {
    increment () {
      // `this` 指向该组件实例
      this.count++
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
  margin: 0 10px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.el-row{
  justify-content: center;
}

</style>