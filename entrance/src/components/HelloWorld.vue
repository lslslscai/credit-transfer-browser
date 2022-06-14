<template>
  <el-button @click="connect">连接区块链</el-button>
  <el-row style="justify-content: center">{{ connectState }}</el-row>

  <el-form :v-model="connection">
    <el-form-item label="服务器IP" :label-width="width">
      <el-input v-model="connection.ip" />
    </el-form-item>
  </el-form>
  <el-button @click="login">管理员登陆</el-button>
  <el-form :model="adminForm">
    <el-form-item label="ID" :label-width="width">
      <el-input v-model="adminForm.schoolID" />
    </el-form-item>
    <el-form-item label="密码" :label-width="width">
      <el-input v-model="adminForm.schoolPwd" type="password"/>
    </el-form-item>
  </el-form>
</template>

<script>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import AElf from "aelf-sdk";
import axios from "axios";
export default {
  setup() {
    const width = "200px";
    const adminForm = reactive({
      schoolID: "00001",
      schoolPwd: "",
    });
    const connection = reactive({
      ip: "127.0.0.1:8001",
    });
    return {
      adminForm: adminForm,
      width: width,
      connection: connection,
    };
  },
  data() {
    return {
      aelf: undefined,
      connectState: "未与区块链链接",
    };
  },
  methods: {
    connect() {
      this.aelf = new AElf(
        new AElf.providers.HttpProvider("http://" + this.connection.ip)
      );
      console.log("http://" + this.connection.ip);
      this.aelf.chain
        .getChainStatus()
        .then((res) => {
          console.log(res);
          if (!this.aelf.isConnected()) {
            this.connectState = "未与区块链链接";
            alert("区块链启动失败！请修改IP或者检查区块链");
          } else {
            this.connectState =
              "区块链链接成功，IP为" + "http://" + this.connection.ip;
            alert("区块链启动成功！");
          }
        })
        .catch((err) => {
          this.connectState = "未与区块链链接";
          alert("区块链启动失败！请修改IP或者检查区块链");
        });
    },
    login() {
      if (this.aelf == undefined) alert("未启动区块链！请先连接到区块链");
      else {
        this.aelf.chain
          .getChainStatus()
          .then((res) => {
            if (!this.aelf.isConnected()) {
              alert("未启动区块链！请先连接到区块链");
            } else {
              console.log(this.aelf.isConnected());
              let formData = new FormData();
              formData.append("schoolID", this.adminForm.schoolID);
              formData.append("schoolPwd", this.adminForm.schoolPwd);
              formData.append("blockchainIP", this.connection.ip);
              formData.append("pushType", "SchoolLogin");
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
                  url: "http://127.0.0.1:8000/api/db_admin/adjust/",
                }).then((res) => {
                  console.log(res.status);
                  if (res.data == "admin login") {
                    alert("超级管理员登陆成功！");
                    this.$router.push(
                      "/admin/" + this.connection.ip.split(":")[1]
                    );
                  } else if (res.data == "login succ!" && res.status == 200) {
                    alert("学校登陆成功！");
                    this.$router.push(
                      "/school/" +
                        this.adminForm.schoolID +
                        "/" +
                        this.connection.ip.split(":")[1]
                    );
                  } else alert("登陆失败！请检查输入是否有误");
                });
              });
            }
          })
          .catch((err) => {
            alert("未启动区块链！请先连接到区块链");
          });
      }
    },
  },
};
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
