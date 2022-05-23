<template>
  <el-dialog
    title="成绩登记"
    v-model="visible"
    width="60%"
    :before-close="handleClose"
    @open="handleOpen"
  >
    <el-form :model="form">
      <el-form-item label="课程编号">
        <el-input v-model="form.courseID" disabled />
      </el-form-item>
      <el-form-item label="课程名称">
        <el-input v-model="form.courseName" disabled />
      </el-form-item>
      <el-form-item label="学生编号">
        <el-input v-model="form.studentID" disabled />
      </el-form-item>
      <el-form-item label="课程名称">
        <el-input v-model="form.studentName" disabled />
      </el-form-item>
      <el-form-item label="成绩">
        <el-input v-model="form.score" @change="calGPA" />
      </el-form-item>
      <el-form-item label="绩点">
        <el-input v-model="form.GPA" disabled />
      </el-form-item>
      <el-form-item>
        <el-checkbox v-model="form.failed">是否挂科</el-checkbox>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="select_cancel">取 消</el-button>
        <el-button type="primary" @click="select_confirm">确 定</el-button>
      </span>
    </template>
  </el-dialog>

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
import { reactive, ref } from "vue";
import axios from "axios";
import Dialog from "./result.vue";
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
  },
  setup() {
    const formLabelWidth = "140px";
    const form = reactive({
      courseID: "",
      courseName: "",
      studentID: "",
      studentName: "",
      score: "",
      GPA: "",
      failed: false,
    });
    return {
      formLabelWidth,
      form,
    };
  },
  data() {
    return {
      dialogTableVisible: false,
      txID: "",
      teacherID: "",
      result: "",
      state: "",
    };
  },
  components: {
    Dialog,
  },
  methods: {
    calGPA() {
      if (this.form.score >= 90) this.form.GPA = 4.0;
      else if (this.form.score >= 85) this.form.GPA = 3.7;
      else if (this.form.score >= 82) this.form.GPA = 3.3;
      else if (this.form.score >= 78) this.form.GPA = 3.0;
      else if (this.form.score >= 75) this.form.GPA = 2.7;
      else if (this.form.score >= 72) this.form.GPA = 2.3;
      else if (this.form.score >= 68) this.form.GPA = 2.0;
      else if (this.form.score >= 64) this.form.GPA = 1.5;
      else if (this.form.score >= 60) this.form.GPA = 1.0;
      else this.form.GPA = 0;
    },
    handleOpen() {
      console.log(this.$props.data[0]);
      this.form.courseID = this.$props.data[0]["courseID"];
      this.form.courseName = this.$props.data[0]["courseName"];
      this.form.studentID = this.$props.data[0]["studentID"];
      this.form.studentName = this.$props.data[0]["studentName"];
      this.form.score = this.$props.data[0]["score"];
      this.form.GPA = this.$props.data[0]["GPA"];
    },
    handleClose(done) {
      this.$confirm("确认关闭？将不保存已做的修改")
        .then((_) => {
          this.$emit("closeDialog");
        })
        .catch((_) => {});
    },
    close_dialog() {
      this.dialogTableVisible = false;
    },
    select_confirm() {
      this.$confirm("确认修改？")
        .then((_) => {
          console.log(this.form);
          axios.defaults.withCredentials = true;
          axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
            console.log(document.cookie);
            let csrf_token = document.cookie.split("=")[1];
            if (document.cookie.indexOf("login") != -1)
              csrf_token = csrf_token.split(";")[0];
            this.teacherID = document.cookie.split("Tealogin=")[1];

            let formData = new FormData();
            formData.append("courseID", this.form.courseID);
            formData.append("studentID", this.form.studentID);
            formData.append("score", this.form.score);
            formData.append("GPA", this.form.GPA);
            formData.append("pushType", "SR_Adjust");
            formData.append("teacherID", this.teacherID);
            formData.append("courseState", true);
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
              this.$emit("closeDialog");
            });
          });
        })
        .catch((_) => {});
    },
    select_cancel() {
      this.$confirm("确认关闭？将不保存已做的修改")
        .then((_) => {
          this.$emit("closeDialog");
        })
        .catch((_) => {});
    },
  },
};
</script>

<style scoped>
.el-button--text {
  margin-right: 15px;
}
.el-select {
  width: 300px;
}
.el-input {
  width: 300px;
}
.dialog-footer button:first-child {
  margin-right: 10px;
}
.el-form {
  height: 400px;
  justify-content: left;
}
</style>
