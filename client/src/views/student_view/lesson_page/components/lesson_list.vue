<template>
  <div class="score_list">
    <el-table
      :data="tableData"
      height="400"
      style="width: 90%"
      @row-click="drop_lesson"
    >
      <el-table-column prop="time" label="开课时间" width="180">
      </el-table-column>
      <el-table-column prop="courseID" label="课程ID" width="180">
      </el-table-column>
      <el-table-column prop="courseName" label="课程名称"> </el-table-column>
      <el-table-column prop="courseType" label="课程类别"> </el-table-column>
      <el-table-column prop="isCompulsory" label="课程性质"> </el-table-column>
      <el-table-column prop="credit" label="学分" width="180">
      </el-table-column>
      <el-table-column prop="courseState" label="课程状态" width="180">
      </el-table-column>
    </el-table>
  </div>

  <Dialog
    v-bind:visible="dialogTableVisible"
    :txID="txID"
    :text="result"
    :state="state"
    :teacherID="teacherID"
    v-on:closeDialog="close_dialog"
  />
</template>

<script>
import axios from "axios";
import Dialog from "../../../../components/dialog/result.vue";
export default {
  props: {
    tableData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      dialogTableVisible: false,
      txID: "",
      result: "",
      state: "",
      teacherID: "",
    };
  },
  components: {
    Dialog,
  },
  methods: {
    close_dialog() {
      this.dialogTableVisible = false;
    },
    drop_lesson(row, column, event) {
      if (row["courseState"] == "结课") {
        this.$confirm("这门课已经结课，不可退课！")
          .then((_) => {})
          .catch((_) => {});
      }
      else if(row["courseState"] == "退课中"){
        this.$confirm("正在退课，请等待结果！")
          .then((_) => {})
          .catch((_) => {});
      }
      else {
        this.$confirm("确认退选这门课吗？")
          .then((_) => {
            axios.defaults.withCredentials = true;
            axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
              console.log(document.cookie);
              let csrf_token = document.cookie.split("=")[1];
              if (document.cookie.indexOf("login") != -1)
                csrf_token = csrf_token.split(";")[0];
              const studentID = document.cookie.split("Stulogin=")[1];

              let formData = new FormData();
              formData.append("courseID", row["courseID"]);
              formData.append("studentID", studentID);
              formData.append("pushType", "SR_Drop");
              axios({
                method: "POST",
                headers: {
                  "X-Requested-With": "XMLHttpRequest",
                  "X-CSRFToken": csrf_token,
                },
                data: formData,
                url: "http://127.0.0.1:8000/api/db_manage/adjust/",
              }).then((res) => {
                console.log(res);
                if (res.data == "drop succ!") {
                  this.result = "修改完成！";
                  this.dialogTableVisible = true;
                  this.state = "no_trans";
                } else {
                  this.result = "修改失败！" + res.data;
                  this.dialogTableVisible = true;
                  this.state = "no_trans";
                }
              });
            });
          })
          .catch((_) => {});
      }
    },
  },
};
</script>
<style scoped>
.el-table {
  margin: 0 auto;
}
</style>