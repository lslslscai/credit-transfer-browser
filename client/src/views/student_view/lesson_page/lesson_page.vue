<template>
  <LessonList v-bind:tableData="scores" />
</template>

<script>
import LessonList from "./components/lesson_list.vue";
import { ref } from "vue";
import axios from "axios";
export default {
  components: {
    LessonList,
  },
  setup() {
    const scores = ref([]);
    let retArray = [];
    console.log(document.cookie);
    let csrf_token = document.cookie.split("=")[1];
    if (document.cookie.indexOf("login") != -1)
      csrf_token = csrf_token.split(";");
    let studentID = document.cookie.split("Stulogin=")[1];
    axios
      .get(
        "http://127.0.0.1:8000/api/db_manage/select/?type=courseRecord&filter=student&value=" +
          studentID
      )
      .then((res) => {
        console.log(res.data)
        res.data.record.forEach((elem) =>{
          retArray.push(elem);
        })
        axios
          .get(
            "http://127.0.0.1:8000/api/db_manage/select/?type=CRCache&filter=" +
              studentID +
              "&action=SR_Select"
          )
          .then((res1) => {
            res1.data.record.forEach((elem) =>{
              retArray.push(elem);
            })
            console.log(retArray)
            retArray.forEach((element) => {
              let courseID = element["courseID"];
              axios
                .get(
                  "http://127.0.0.1:8000/api/db_manage/select/?type=course&filter=" +
                    courseID
                )
                .then((res2) => {
                  console.log(res2.data["course"])
                  element["courseName"] = res2.data["course"]["courseName"];
                  element["credit"] = res2.data["course"]["credit"];
                  element["courseType"] = res2.data["course"]["courseType"];
                  element["isCompulsory"] = res2.data["course"][
                    "isCompulsory"
                  ]
                    ? "必修"
                    : "选修";
                  element["time"] = res2.data["course"]["protocol"]["startDate"];
                  if (element["pushType"] == "SR_Select") {
                    element["courseState"] = "申请中";
                  }
                  else if(element["pushType"] == "SR_Drop"){
                    element["courseState"] = "退课中";
                  }
                  else {
                    element["courseState"] = element["courseState"]
                      ? "结课"
                      : "在读";
                  }

                  scores.value.push(element);
                  console.log(scores.value);
                });
            });
          });
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
