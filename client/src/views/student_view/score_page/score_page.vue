<template>
  <ScoreList v-bind:tableData="scores"/>
</template>

<script>
  import ScoreList from "./components/score_list.vue"
  export default {
    components: {
      ScoreList
    },
    data() {
      return{
        scores:[
          {
            time:"2020-2021-1",
            courseName: "高等数学", courseID: "100562160001",
            courseType: "数学", isCompulsory: "必修",
            credit:5, score: 91, GPA: 4.0
          },
          {
            time:"2020-2021-1",
            courseName: "程序设计原理", courseID: "100562160001",
            courseType: "专业必修课", isCompulsory: "必修",
            credit:3, score: 89, GPA: 3.6
          },
          {
            time:"2020-2021-1",
            courseName: "高等数学", courseID: "100562160001",
            courseType: "数学", isCompulsory: "必修",
            credit:5, score: 91, GPA: 4.0
          },
        ]
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
