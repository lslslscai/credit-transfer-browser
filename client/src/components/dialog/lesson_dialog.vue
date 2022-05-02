<template>
  <el-dialog
    title="提示"
    v-model="visible"
    width="50%"
    :before-close="handleClose"
  >
    <span>{{ text }}</span>
    <el-table :data="data">
      <el-table-column prop="courseID" label="课程ID" width="180">
      </el-table-column>
      <el-table-column prop="courseName" label="课程名称"> </el-table-column>
      <el-table-column prop="school" label="所属学校" width="180">
      </el-table-column>
      <el-table-column prop="college" label="开课学院" width="180">
      </el-table-column>
      <el-table-column prop="capacity" label="课程容量" width="180">
      </el-table-column>
      <el-table-column prop="selected" label="已选课" width="180">
      </el-table-column>
    </el-table>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="select_cancel">取 消</el-button>
        <el-button type="primary" @click="select_confirm">确 定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import axios from "axios";

export default {
  emits: ["closeDialog"],
  props: {
    data: {
      type: Array,
      required: true,
    },
    visible: {
      type: Boolean,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
  },
  data() {
    return {};
  },
  methods: {
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },
    select_confirm() {
      this.$confirm("确定选这门课了吗？")
        .then((_) => {
          axios.defaults.withCredentials = true;
          axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
            console.log(document.cookie);
            let csrf_token = document.cookie.split("=")[1];
            if (document.cookie.indexOf("login") != -1)
              csrf_token = csrf_token.split(";")[0];
            const studentID = document.cookie.split("Stulogin=")[1];
            let protocol = JSON.stringify({
              "startDate": this.data[0]["protocol"].startDate,
              "projectDate": this.data[0]["protocol"].projectDate,
              "testDate": this.data[0]["protocol"].testDate,
              "rateOfTest": this.data[0]["protocol"].rateOfTest,
              "rateOfProject": this.data[0]["protocol"].rateOfProject,
            });
            let formData = new FormData();
            formData.append("courseID", this.data[0]['courseID']);
            formData.append("studentID", studentID);
            formData.append("protocol", protocol);
            formData.append("note", studentID+" selects "+this.data[0]['courseID'])
            formData.append("pushType", "SR_Select")
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
              this.$emit("closeDialog");
            });
          })
        })
        .catch((_) => {});
    },
    select_cancel() {
      this.$confirm("确认关闭？")
        .then((_) => {
          this.$emit("closeDialog");
        })
        .catch((_) => {});
    },
  },
};
</script>
