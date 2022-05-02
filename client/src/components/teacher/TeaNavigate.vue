<template>
  <el-menu
    :default-active="$route.path"
    class="top-navigation"
    mode="horizontal"
    @select="handleSelect"
    background-color="#fff"
    text-color="#000"
    active-text-color="#245086"
    router
  >
    <el-menu-item index="/admin/main" route="/admin/main">首页</el-menu-item>
    <el-sub-menu index="2">
      <template #title>课程管理</template>
      <el-menu-item index="/admin/main/course" route="/admin/main/course"
        >课程总览</el-menu-item
      >
      <el-menu-item
        index="/admin/main/course/add"
        route="/admin/main/course/add"
        >添加课程</el-menu-item
      >
    </el-sub-menu>
    <el-sub-menu index="3">
      <template #title>学生管理</template>
      <el-menu-item index="/admin/main/student" route="/admin/main/student"
        >学生总览</el-menu-item
      >
      <el-menu-item
        index="/admin/main/student/add"
        route="/admin/main/student/add"
        >添加学生</el-menu-item
      >
    </el-sub-menu>
    <el-menu-item index="/admin/main/scoure_admin">成绩登记</el-menu-item>
    <el-menu-item index="5">登出</el-menu-item>
  </el-menu>
</template>

<script>
import VueCookies from "vue-cookies";
import axios from "axios";
const logout = () => {
  let formData = new FormData();
  formData.append("teacherID", document.cookie.split("login=")[1]);
  formData.append("pwd", "undefined");
  formData.append("pushType", "Tea_Logout");
  console.log(document.cookie.split("login=")[1]);
  axios.defaults.withCredentials = true;
  axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
    console.log(document.cookie);
    let csrf_token = document.cookie.split("=")[1];
    axios({
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrf_token,
      },
      data: formData,
      url: "http://127.0.0.1:8000/api/db_manage/adjust/",
    }).then((res) => {
      if (res.data == "logout succ") VueCookies.VueCookies.remove("login");
    });
  });
};

export default {
  data() {
    return {
      activeIndex: "1",
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
      if (key == "5") {
        logout();
        this.$router.push("/admin");
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-menu--horizontal {
  margin: 1rem 0px 3rem 3rem;
}
.el-menu--horizontal > .el-menu-item {
  margin-right: 0.5rem;
  text-align: center;
}

.el-menu--horizontal > .el-menu-item.is-active {
  background-color: #245086 !important;
  color: #fff !important;
}

.el-menu--horizontal > .el-sub-menu {
  margin-right: 0.5rem;
  border-bottom: none;
  text-align: center;
}

.el-menu--horizontal > .el-sub-menu.is-active {
  background-color: #245086 !important;
  color: #fff !important;
}

.el-menu-item:hover {
  background-color: #245086 !important;
  color: #fff !important;
}

.el-menu-item.is-active {
  background-color: #245086 !important;
  color: #fff !important;
}
</style>
