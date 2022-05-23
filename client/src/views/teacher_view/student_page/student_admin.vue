<template>
  <studentList v-bind:tableData="student" />
</template>
<script>
import { ref } from "vue";
import studentList from "./components/student_list.vue";
import axios from "axios";
export default {
  components: {
    studentList,
  },
  setup() {
    const student = ref([]);
    let csrf_token = document.cookie.split("=")[1];
    if (document.cookie.indexOf("login") != -1)
      csrf_token = csrf_token.split(";")[0];
    let teacherID = document.cookie.split("Tealogin=")[1];
    const reg = "^" + teacherID.substring(0,5)+"([0-9]{4,})"+ teacherID.substring(5,8)
    axios
      .get(
        "http://127.0.0.1:8000/api/db_manage/select/?type=student&filter="+ reg
      )
      .then(
        (res) => (
          (student.value = res.data.student), console.log(student.value)
        )
      );
    return {
      student,
    };
  },
  data() {
    return {};
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
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
.el-row {
  justify-content: center;
}
</style>
