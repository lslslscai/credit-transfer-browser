<template>
  <el-form :model="form" label-width="100px">
    <el-form-item label="学生编号">
      <el-input v-model="form.studentID" @change="autoComplete" />
    </el-form-item>
    <el-form-item label="学生姓名">
      <el-input v-model="form.studentName" />
    </el-form-item>
    <el-form-item label="学校">
      <el-input v-model="form.school" />
    </el-form-item>
    <el-form-item label="学院">
      <el-input v-model="form.college" />
    </el-form-item>
    <el-form-item label="在读学历">
      <el-select v-model="form.type">
        <el-option value="本科生" />
        <el-option value="研究生" />
        <el-option value="博士生" />
      </el-select>
    </el-form-item>
  </el-form>
  <el-button type="primary" @click="submit">提交</el-button>

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
import { ref, reactive } from "vue";
import axios from "axios";
import Dialog from "../../../components/dialog/result.vue"
export default {
  setup() {
    const form = reactive({
      studentID: "100013018001004",
      studentName: "王五",
      school: "xx大学",
      college: "计算机学院",
      type: "本科生",
    });
    return {
      form,
    };
  },
  data() {
    return {
      dialogTableVisible: false,
      txID: "",
      teacherID:"",
      result: "",
      state: "",
    };
  },
  components: {
    Dialog,
  },
  methods: {
    autoComplete() {
      var schoolID = this.form.studentID.substring(0, 5);
      var collegeID = this.form.studentID.substring(9, 12);
      console.log(schoolID, collegeID);
      axios
        .get(
          "http://127.0.0.1:8000/api/db_manage/select/?type=school&filter=" +
            schoolID
        )
        .then((res) => (this.form.school = res.data.school));
      axios
        .get(
          "http://127.0.0.1:8000/api/db_manage/select/?type=college&filter=" +
            collegeID
        )
        .then((res) => (this.form.college = res.data.college));
    },
    close_dialog() {
      this.dialogTableVisible = false;
    },
    submit() {
      axios.defaults.withCredentials = true;
      axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
        console.log(document.cookie);
        let csrf_token = document.cookie.split("=")[1];
        if (document.cookie.indexOf("login") != -1)
          csrf_token = csrf_token.split(";")[0];
        this.teacherID = document.cookie.split("Tealogin=")[1];

        let formData = new FormData();
        formData.append("studentID", this.form.studentID);
        formData.append("studentName", this.form.studentName);
        formData.append("school", this.form.school);
        formData.append("college", this.form.college);
        formData.append("type", this.form.type);
        formData.append("pwd", this.form.studentID);
        formData.append("studentState", "在读");
        formData.append("state", 0);
        formData.append("pushType", "SRT_Register");
        formData.append("teacherID", this.teacherID);

        axios({
          method: "POST",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf_token,
          },
          data: formData,
          url: "http://127.0.0.1:8000/api/db_manage/adjust/",
        }).then((res) => {
          console.log(res.data);
          if (res.data["txRet"] != undefined) {
            this.txID = res.data["txRet"];
            console.log(this.txID);
            this.result = "修改完成！请检查区块链交易结果";
            this.dialogTableVisible = true;
            this.state = "db_succ";
          } else {
            this.result = "修改失败！" + res.data;
            this.dialogTableVisible = true;
            this.state = "db_fail";
          }
        });
      });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-form {
  margin: 0, auto;
  width: 60%;
}
</style>
