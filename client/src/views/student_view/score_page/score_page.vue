<template>
  <ScoreList v-bind:tableData="scores" />
</template>

<script>
import ScoreList from "./components/score_list.vue";
import { ref } from "vue";
import axios from "axios";
export default {
  components: {
    ScoreList,
  },
  setup() {
    const scores = ref([]);
    console.log(document.cookie);
    let csrf_token = document.cookie.split("=")[1];
    if (document.cookie.indexOf("login") != -1)
      csrf_token = csrf_token.split(";")[0];
    let studentID = document.cookie.split("Stulogin=")[1];
    axios
      .get(
        "http://127.0.0.1:8000/api/db_manage/select/?type=courseRecord&filter=student&value=" +
          studentID
      )
      .then((res) => {
        scores.value = res.data.record;
        scores.value.forEach((element) => {
          let courseID = element["courseID"];
          axios
            .get(
              "http://127.0.0.1:8000/api/db_manage/select/?type=course&filter=" +
                courseID
            )
            .then((res) => {
              element["courseName"] = res.data["course"]["courseName"];
              element["credit"] = res.data["course"]["credit"];
              element["courseType"] = res.data["course"]["courseType"];
              element["isCompulsory"] = res.data["course"]["isCompulsory"]
                ? "必修"
                : "选修";
              element["time"] = res.data["course"]["protocol"]["startDate"];
            });
        });
        console.log(scores.value);
      });
    return {
      scores,
    };
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
