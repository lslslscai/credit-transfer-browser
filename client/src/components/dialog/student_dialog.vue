<template>
  <el-dialog
    title="学生修改"
    v-model="visible"
    width="60%"
    :before-close="handleClose"
    @open="handleOpen"
  >
    <span>{{ text }}</span>
    <el-form :model="form">
      <el-form-item label="学生编号" :label-width="formLabelWidth">
        <el-input v-model="form.studentID" disabled />
      </el-form-item>
      <el-form-item label="学生姓名" :label-width="formLabelWidth">
        <el-input v-model="form.studentName" />
      </el-form-item>
      <el-form-item label="学生状态" :label-width="formLabelWidth">
        <el-select
          v-model="form.studentState"
          placeholder="Please select a zone"
        >
          <el-option value="在读" />
          <el-option value="毕业" />
          <el-option value="退学" />
        </el-select>
      </el-form-item>
      <el-form-item label="学校" :label-width="formLabelWidth">
        <el-input v-model="form.school" />
      </el-form-item>
      <el-form-item label="学院" :label-width="formLabelWidth">
        <el-input v-model="form.college" />
      </el-form-item>
      <el-form-item label="在读学历" :label-width="formLabelWidth">
        <el-select v-model="form.type" placeholder="Please select a zone">
          <el-option value="本科生" />
          <el-option value="研究生" />
          <el-option value="博士生" />
        </el-select>
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
import Dialog from "./result.vue"
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
  setup() {
    const formLabelWidth = "140px";
    const form = reactive({
      studentID: "",
      studentName: "",
      studentState: "",
      school: "",
      college: "",
      type: "",
    });
    return {
      form,
      formLabelWidth,
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
    handleOpen() {
      console.log(this.$props.data[0]);
      this.form.studentID = this.$props.data[0]["studentID"];
      this.form.studentName = this.$props.data[0]["studentName"];
      this.form.studentState = this.$props.data[0]["studentState"];
      this.form.school = this.$props.data[0]["school"];
      this.form.college = this.$props.data[0]["college"];
      this.form.type = this.$props.data[0]["type"];
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
      this.$confirm("确认修改")
        .then((_) => {
          axios.defaults.withCredentials = true;
          axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
            console.log(document.cookie);
            let csrf_token = document.cookie.split("=")[1];
            if (document.cookie.indexOf("login") != -1)
              csrf_token = csrf_token.split(";")[0];
            this.teacherID = document.cookie.split("Tealogin=")[1];

            let formData = new FormData();
            formData.append("studentID", this.$props.data[0]["studentID"]);
            formData.append("studentName", this.form.studentName);
            formData.append("school", this.form.school);
            formData.append("college", this.form.college);
            formData.append("type", this.form.type);
            formData.append("studentState", this.form.studentState);
            formData.append("pwd", this.form.studentID);
            formData.append("state", 0);
            formData.append("pushType", "SRT_Adjust");
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
