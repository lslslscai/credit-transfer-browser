<template>
  <div>
    <LessonList v-bind:tableData="lesson"/>
  </div>
</template>

<script>
import { ref } from 'vue'
  import LessonList from "./components/lesson_list.vue"
  import axios from 'axios'
  export default {
    components: {
      LessonList
    },
    setup(){
      const lesson = ref([])
      axios.get("http://127.0.0.1:8000/api/db_manage/select/?type=course&filter=all")
      .then(res => (
        lesson.value = res.data.course,
        console.log(lesson.value)
      ))
      return{
        lesson
      }
    },
    data() {
      return{
      }
    },
    methods:{
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
