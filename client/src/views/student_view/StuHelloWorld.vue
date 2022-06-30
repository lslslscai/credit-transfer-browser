<template>
  <div class="hello">
    <br/><br/><br/>
    <img alt="Vue logo" src="../../assets/logo.jpg"/>
    <br/><br/>
    <h1>{{ text }}</h1>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
  data() {
    return {
      count: 0,
      text:"欢迎进入跨校学习管理系统！"
    };
  },
  methods: {
    increase() {
      this.count++;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
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
</style>

