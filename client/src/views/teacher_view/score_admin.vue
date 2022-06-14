<template>
  <el-select
    v-model="schoolID"
    placeholder="学校"
    clearable
    @change="getCourse"
  >
    <el-option
      v-for="item in schools"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
  <el-select
    v-model="collegeID"
    placeholder="学院"
    clearable
    @change="getCourse"
  >
    <el-option
      v-for="item in colleges"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
  <el-select
    v-model="courseID"
    :disabled="courseDisable"
    clearable
    placeholder="课程"
    @change="getCourseRecord"
  >
    <el-option
      v-for="item in courses"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
  <el-table
    :data="tableData"
    height="400"
    style="width: 90%"
    @row-click="scoreModify"
  >
    <el-table-column prop="time" label="开课时间" width="180">
    </el-table-column>
    <el-table-column prop="courseID" label="课程ID" width="180">
    </el-table-column>
    <el-table-column prop="courseName" label="课程名称"> </el-table-column>
    <el-table-column prop="studentID" label="学生ID"> </el-table-column>
    <el-table-column prop="studentName" label="学生姓名"> </el-table-column>
    <el-table-column prop="score" label="成绩" width="180"> </el-table-column>
    <el-table-column prop="GPA" label="绩点" width="180"> </el-table-column>
  </el-table>

  <Dialog
    v-bind:data="selectedData"
    :visible="dialogTableVisible"
    v-on:closeDialog="close_dialog"
  />
</template>

<script>
import Dialog from "../../components/dialog/score_modify.vue";
import { ref } from "@vue/reactivity";
import axios from "axios";

export default {
  components:{
    Dialog
  },
  setup() {
    const schools = ref([]);
    const colleges = ref([]);
    const courses = ref([]);
    axios
      .get("http://127.0.0.1:8000/api/db_manage/select/?type=school&filter=all")
      .then((res) => {
        res.data.school.forEach((element) => {
          schools.value.push({
            value: element["schoolID"],
            label: element["schoolName"],
          });
        });
      });
    axios
      .get(
        "http://127.0.0.1:8000/api/db_manage/select/?type=college&filter=all"
      )
      .then((res) => {
        res.data.college.forEach((element) => {
          colleges.value.push({
            value: element["collegeID"],
            label: element["collegeName"],
          });
        });
      });
    return {
      schools,
      colleges,
      courses,
    };
  },
  data() {
    return {
      courseDisable: true,
      dialogTableVisible: false,
      schoolID: "",
      collegeID: "",
      courseID: "",
      tableData: [],
      selectedData: []
    };
  },
  methods: {
    getCourse() {
      if (this.schoolID != "" && this.collegeID != "") {
        this.courseDisable = false;
        let regex = "^" + this.schoolID + this.collegeID;
        console.log(regex);
        axios
          .get(
            "http://127.0.0.1:8000/api/db_manage/select/?type=course&filter=" +
              regex
          )
          .then((res) => {
            console.log(res);
            res.data.course.forEach((element) => {
              this.courses.push({
                value: element["courseID"],
                label: element["courseName"],
              });
            });
          });
      } else {
        this.courseDisable = true;
      }
    },
    getCourseRecord() {
      if (this.courseID != "") {
        axios
          .get(
            "http://127.0.0.1:8000/api/db_manage/select/?type=courseRecord&filter=AllCourse&value=" +
              this.courseID
          )
          .then((res) => {
            console.log(res);
            this.tableData = res.data.record;
            this.tableData.forEach((element) => {
              axios
                .get(
                  "http://127.0.0.1:8000/api/db_manage/select/?type=course&filter=" +
                    this.courseID
                )
                .then((res) => {
                  element["courseName"] = res.data["course"]["courseName"];
                  element["time"] = res.data["course"]["protocol"]["startDate"];
                });
              axios
                .get(
                  "http://127.0.0.1:8000/api/db_manage/select/?type=student&filter=" +
                    element["studentID"]
                )
                .then((res) => {
                  element["studentName"] = res.data["student"]["studentName"];
                });
            });
          });
      } else {
        this.tableData = [];
      }
    },
    scoreModify(row, column, event){
      this.selectedData.pop();
      this.selectedData.push(row);
      console.log(this.selectedData);
      this.dialogTableVisible = true;
    },
    close_dialog() {
      this.dialogTableVisible = false;
    },
  },
};
</script>

<style scoped>
.el-table {
  margin: 0 auto;
}
</style>