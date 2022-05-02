<template>
  <el-form :model="form" class="rootForm" label-position="left">
    <el-form :inline="true" label-width="80px" label-postion="left">
      <el-form-item label="课程编号">
        <el-input
          class="inlineInput"
          v-model="form.courseID"
          @change="autoComplete"
        />
      </el-form-item>
      <el-form-item label="课程名称">
        <el-input class="inlineInput" v-model="form.courseName" />
      </el-form-item>
    </el-form>
    <el-form :inline="true" label-width="80px" label-postion="left">
      <el-form-item class="inlineSelects" label="课程性质">
        <el-switch
          class="inlineSelects"
          v-model="form.isCompulsory"
          active-color="#13ce66"
          inactive-color="#ff4949"
          :active-value="true"
          :inactive-value="false"
          active-text="必修"
          inactive-text="选修"
        />
      </el-form-item>
      <el-form-item label="是否开设">
        <el-switch
          class="inlineSelects"
          v-model="form.isValid"
          active-color="#13ce66"
          inactive-color="#ff4949"
          :active-value="true"
          :inactive-value="false"
          active-text="是"
          inactive-text="否"
        />
      </el-form-item>
      <el-form-item label="课程类别">
        <el-select class="inlineSelects" v-model="form.courseType">
          <el-option value="课内课程" />
          <el-option value="校内跨专业课程" />
          <el-option value="跨校课程" />
          <el-option value="课外课程" />
        </el-select>
      </el-form-item>
    </el-form>
    <el-form :inline="true" label-width="80px" label-postion="left">
      <el-form-item label="所属学校">
        <el-input class="inlineInput" v-model="form.school" />
      </el-form-item>
      <el-form-item label="开课学院">
        <el-input class="inlineInput" v-model="form.college" />
      </el-form-item>
    </el-form>

    <el-form :inline="true" label-width="80px" label-postion="left">
      <el-form-item label="课程容量">
        <el-input class="inlineInput" v-model="form.capacity" />
      </el-form-item>
      <el-form-item label="学分">
        <el-input class="inlineInput" v-model="form.credit" />
      </el-form-item>
    </el-form>

    <el-form :inline="true" label-width="100px" label-postion="left">
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
    <el-form :inline="true" label-width="80px" label-postion="left">
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
  <el-button type="primary" size="large" @click="submit">提交</el-button>
</template>
<script>
import { ref, reactive } from "vue";
import axios from "axios";
export default {
  setup() {
    const form = reactive({
      courseID: "100562160003",
      courseName: "计算机组成原理",
      isCompulsory: true,
      isValid: true,
      school: "天津大学",
      college: "智能与计算学部",
      courseType: "课内课程",
      capacity: "100",
      credit: "3",
      protocol: {
        startDate: new Date(),
        projectDate: new Date(),
        testDate: new Date(),
        rateOfTest: 0.6,
        rateOfProject: 0.3,
      },
    });
    return {
      form,
    };
  },
  methods: {
    autoComplete() {
      var schoolID = this.form.courseID.substring(0, 5);
      var collegeID = this.form.courseID.substring(5, 8);
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
    dateTrans(raw) {
      let date = (raw.getDate() < 10 ? "0" : "") + raw.getDate();
      let month = (raw.getMonth() + 1 < 10 ? "0" : "") + (raw.getMonth() + 1);
      let ret = raw.getFullYear() + "-" + month + "-" + date;
      console.log(ret);
      return ret;
    },
    submit() {
      let start = this.dateTrans(this.form.protocol.startDate);
      let test = this.dateTrans(this.form.protocol.testDate);
      let project = this.dateTrans(this.form.protocol.projectDate);
      axios.defaults.withCredentials = true;
      axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
        console.log(document.cookie);
        let csrf_token = document.cookie.split("=")[1];
        if (document.cookie.indexOf("login") != -1)
          csrf_token = csrf_token.split(";")[0];
        let teacherID = document.cookie.split("Tealogin=")[1];
        let protocol = JSON.stringify({
          "startDate": start,
          "projectDate": project,
          "testDate": test,
          "rateOfTest": this.form.protocol.rateOfTest,
          "rateOfProject": this.form.protocol.rateOfProject,
        });
        let formData = new FormData();
        formData.append("courseID", this.form.courseID);
        formData.append("courseName", this.form.courseName);
        formData.append("school", this.form.school);
        formData.append("college", this.form.college);
        formData.append("courseType", this.form.courseType);
        formData.append("isCompulsory", this.form.isCompulsory);
        formData.append("isValid", this.form.isValid);
        formData.append("capacity", this.form.capacity);
        formData.append("pushType", "Course_Create");
        formData.append("teacherID", teacherID);
        formData.append("credit", this.form.credit);
        formData.append("protocol", protocol);
        console.log(formData);
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
        });
      });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-form.rootForm {
  margin-left: 5rem;
  text-align: left;
  width: 80%;
}
.el-input.inlineInput {
  width: 20rem;
  margin-right: 2rem;
}
.el-switch.inlineSelects {
  margin-right: 18px;
}
.el-select.inlineSelects {
  margin-right: 22px;
}
</style>
