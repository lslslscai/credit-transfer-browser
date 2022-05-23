<template>
  <el-dialog
    title="课程修改"
    v-model="visible"
    width="60%"
    :before-close="handleClose"
    @open="handleOpen"
  >
    <span>{{ text }}</span>
    <el-form :model="form" class="rootForm">
      <el-form :inline="true">
        <el-form-item label="课程编号">
          <el-input v-model="form.courseID" />
        </el-form-item>
        <el-form-item label="课程名称">
          <el-input v-model="form.courseName" />
        </el-form-item>
      </el-form>
      <el-form :inline="true"></el-form>
      <el-form :inline="true">
        <el-form-item label="所属学校">
          <el-input v-model="form.school" />
        </el-form-item>
        <el-form-item label="开课学院">
          <el-input v-model="form.college" />
        </el-form-item>
      </el-form>
      <el-form :inline="true">
        <el-form-item label="课程容量">
          <el-input v-model="form.capacity" />
        </el-form-item>
        <el-form-item label="学分">
          <el-input v-model="form.credit" />
        </el-form-item>
      </el-form>
      <el-form :inline="true">
        <el-form-item label="课程性质">
          <el-switch
            v-model="form.isCompulsory"
            active-color="#13ce66"
            inactive-color="#ff4949"
            :active-value="true"
            :inactive-value="false"
            active-text="必修"
            inactive-text="选修"
          />
        </el-form-item>
        <el-form-item label="课程类别">
          <el-select v-model="form.courseType">
            <el-option value="课内课程" />
            <el-option value="校内跨专业课程" />
            <el-option value="跨校课程" />
            <el-option value="课外课程" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否开设">
          <el-switch
            v-model="form.isValid"
            active-color="#13ce66"
            inactive-color="#ff4949"
            :active-value="true"
            :inactive-value="false"
            active-text="是"
            inactive-text="否"
          />
        </el-form-item>
      </el-form>
      <el-form :inline="true">
        <el-form-item label="开始日期">
          <el-date-picker v-model="form.protocol.startDate" type="date" />
        </el-form-item>
        <el-form-item label="考试日期">
          <el-date-picker v-model="form.protocol.testDate" type="date" />
        </el-form-item>
        <el-form-item label="实践截至日期">
          <el-date-picker v-model="form.protocol.projectDate" type="date" />
        </el-form-item>
      </el-form>
      <el-form :inline="true">
        <el-form-item label="考试占比">
          <el-input-number
            v-model="form.protocol.rateOfTest"
            :precision="2"
            :step="0.01"
            :max="1"
          />
        </el-form-item>
        <el-form-item label="实验占比">
          <el-input-number
            v-model="form.protocol.rateOfProject"
            :precision="2"
            :step="0.01"
            :max="1"
          />
        </el-form-item>
      </el-form>
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
      courseID: "",
      courseName: "",
      isCompulsory: true,
      isValid: true,
      school: "",
      college: "",
      courseType: "",
      capacity: "",
      credit: "",
      selected:"",
      protocol: {
        startDate: new Date(),
        projectDate: new Date(),
        testDate: new Date(),
        rateOfTest: 0.6,
        rateOfProject: 0.3,
      },
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
      result: "",
      state: "",
      teacherID:""
    };
  },
  components: {
    Dialog,
  },
  methods: {
    handleOpen() {
      console.log(this.$props.data[0]);
      this.form.courseID = this.$props.data[0]["courseID"];
      this.form.courseName = this.$props.data[0]["courseName"];
      this.form.isCompulsory = this.$props.data[0]["isCompulsory"];
      this.form.school = this.$props.data[0]["school"];
      this.form.college = this.$props.data[0]["college"];
      this.form.courseType = this.$props.data[0]["courseType"];
      this.form.isValid = this.$props.data[0]["isValid"];
      this.form.capacity = this.$props.data[0]["capacity"];
      this.form.selected = this.$props.data[0]["selected"];
      this.form.credit = this.$props.data[0]["credit"];
      this.form.protocol.startDate =
        this.$props.data[0]["protocol"]["startDate"];
      this.form.protocol.projectDate = this.$props.data[0].protocol.projectDate;
      this.form.protocol.testDate = this.$props.data[0]["protocol"]["testDate"];
      this.form.protocol.rateOfTest =
        this.$props.data[0]["protocol"]["rateOfTest"];
      this.form.protocol.rateOfProject =
        this.$props.data[0]["protocol"]["rateOfProject"];
    },
    close_dialog() {
      this.dialogTableVisible = false;
    },
    handleClose(done) {
      this.$confirm("确认关闭？将不保存已做的修改")
        .then((_) => {
          this.$emit("closeDialog");
        })
        .catch((_) => {});
    },
    select_confirm() {
      this.$confirm("确认修改？")
        .then((_) => {
          axios.defaults.withCredentials = true;
          axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
            console.log(document.cookie);
            let csrf_token = document.cookie.split("=")[1];
            if (document.cookie.indexOf("login") != -1)
              csrf_token = csrf_token.split(";")[0];
            this.teacherID =document.cookie.split("Tealogin=")[1];

            let formData = new FormData();
            formData.append("courseID", this.form.courseID);
            formData.append("courseName", this.form.courseName);
            formData.append("school", this.form.school);
            formData.append("college", this.form.college);
            formData.append("courseType", this.form.courseType);
            formData.append("isCompulsory", this.form.isCompulsory);
            formData.append("isValid", this.form.isValid);
            formData.append("capacity", this.form.capacity);
            formData.append("selected", this.form.selected);
            formData.append("pushType", "Course_Modify");
            formData.append("teacherID", this.teacherID);
            formData.append("credit", this.form.credit);
            formData.append("protocol", JSON.stringify(this.form.protocol));
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
.el-form.rootForm {
  justify-content: left;
}
</style>
