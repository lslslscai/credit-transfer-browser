<template>
  <el-row>
    <h1>欢迎进入跨校学习管理系统（教师端）</h1>
  </el-row>
  <el-form
    ref="ruleFormRef"
    :model="ruleForm"
    status-icon
    :rules="rules"
    label-width="120px"
    class="demo-ruleForm"
    style="width: 50%"
  >
    <el-form-item label="教师编号" prop="teacherID">
      <el-input v-model.number="ruleForm.teacherID" />
    </el-form-item>
    <el-form-item label="密码" prop="pwd">
      <el-input v-model="ruleForm.pwd" type="password" autocomplete="off" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)"
        >Submit</el-button
      >
      <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import {useRouter} from "vue-router";
import type { FormInstance } from "element-plus";
import axios from "axios";

const ruleFormRef = ref<FormInstance>();

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("Please input the password"));
  }
  callback();
};

const ruleForm = reactive({
  pwd: "",
  teacherID: "",
});

const rules = reactive({
  pwd: [{ validator: validatePass, trigger: "blur" }],
});

const r = useRouter()

const submitForm = (formEl: FormInstance | undefined) => {

  if (!formEl) return;
  if(document.cookie.includes("login")){
    alert("已经登陆了！")
    resetForm(formEl);
    if(document.cookie.includes("Stulogin"))
      r.push({path: "/home"})
    else if(document.cookie.includes("Tealogin"))
      r.push({path: "/admin/main"})
    return;
  }
  formEl.validate((valid) => {
    if (valid) {
      let formData = new FormData();
      formData.append("pwd", formEl.$props.model.pwd);
      formData.append("teacherID", formEl.$props.model.teacherID);
      formData.append("pushType","Login");
      axios.defaults.withCredentials = true;
      axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
        console.log(document.cookie)
        let csrf_token = document.cookie.split("=")[1]
        axios({
            method:'POST',
            headers:{
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': csrf_token
            },
            data: formData,
            url: 'http://127.0.0.1:8000/api/db_manage/adjust/'
          }
        ).then(res =>{
          resetForm(formEl);
          if(res.data.includes("succ")){
            r.push({path: "/admin/main"})
          }
        })
      })
    } else {
      console.log("error submit!");
      resetForm(formEl);
      return false;
    }
  });
};

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
};
</script>

<style scoped>
.el-form {
  margin: 0 auto;
}
.el-form-item {
  margin-bottom: 2rem !important;
}

h1,
h2 {
  margin:10rem auto;
}
</style>