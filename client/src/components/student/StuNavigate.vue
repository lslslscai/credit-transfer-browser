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
    <el-menu-item index="/home" route="/home">首页</el-menu-item>
    <el-sub-menu index="2">
      <template #title>个人信息</template>
      <el-menu-item index="/home/personal_page" route="/home/personal_page"
        >我的信息</el-menu-item
      >
      <el-menu-item
        index="/home/personal_page/score"
        route="/home/personal_page/score"
        >我的成绩</el-menu-item
      >
    </el-sub-menu>
    <el-sub-menu index="3">
      <template #title>课程管理</template>
      <el-menu-item index="/home/course/" route="/home/course"
        >我的课程</el-menu-item
      >
      <el-menu-item index="/home/course/select/" route="/home/course/select"
        >选课</el-menu-item
      >
    </el-sub-menu>
    <el-menu-item index="5">登出</el-menu-item>
  </el-menu>
</template>

<script>
import VueCookies from 'vue-cookies';
import axios from 'axios'
const logout = () => {
  let formData = new FormData();
  formData.append("studentID", document.cookie.split("login=")[1]);
  formData.append("pwd", "undefined")
  formData.append("pushType", "Stu_Logout");
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
    }).then(res =>{
      if(res.data == "logout succ")
        VueCookies.VueCookies.remove("login")
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
        logout()
        this.$router.push("/login");
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
