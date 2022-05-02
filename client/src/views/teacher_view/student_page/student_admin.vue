<template>
  <studentList v-bind:tableData="student"/>
</template>
<script>
  import { ref } from 'vue'
  import studentList from "./components/student_list.vue"
  import axios from 'axios'
  export default {
    components: {
      studentList
    },
    setup(){
      const student = ref([])
      axios.get("http://127.0.0.1:8000/api/db_manage/select/?type=student&filter=all")
      .then(res => (
        student.value = res.data.student,
        console.log(student.value)
      ))
      return{
        student
      }
    },
    data() {
      return {}
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
