<template>
  <h1>{{ msg }}</h1>
  <el-button @click="check">查看链状态</el-button>
  <el-button @click="addSchool">添加学校</el-button>
  <el-button @click="addTeacher">添加教师</el-button>
  <el-button @click="addCollege">添加学院</el-button>
  <br />
  <el-button @click="getSchool">查看学校</el-button>
  <el-button @click="getTeacher">查看教师</el-button>

</template>

<script>
import { ref } from "vue";
import AElf from "aelf-sdk";
import axios from "axios";

var url = "mongodb://localhost:27017";

const adminPriKey =
  "6fb5eee18c69b147b4f75a0cfc640ea457f69741e7e3c3f07eede7348dba0c9b";
const CRAddress = "2LUmicHyH4RXrMjG4beDwuDsiWJESyLkgkwPdGTR8kahRzq5XS";

export default {
  props: {
    msg: String,
  },
  setup() {
    const count = ref(0);
    const aelf = new AElf(
      new AElf.providers.HttpProvider("http://127.0.0.1:1235")
    );
    if (!aelf.isConnected()) console.log("Blockchain Node is not running.");
    const adminWallet = AElf.wallet.getWalletByPrivateKey(adminPriKey);
    return {
      aelf: aelf,
      wallet: adminWallet,
      count: count,
    };
  },
  methods: {
    check() {
      console.log(this.aelf.isConnected());
    },
    addSchool() {
      let CRContract;
      (async () => {
        // get chain status
        CRContract = await this.aelf.chain.contractAt(CRAddress, this.wallet);
        console.log(CRContract);
        var schoolInfo = {
          schoolID: "10056",
          schoolAddress: this.wallet.address,
          rating: 0,
        };
        let formData = new FormData();
        formData.append("schoolID", "10056")
        formData.append("schoolName", "天津大学")
        CRContract.School_Register(schoolInfo).then((txID) => {
          console.log(txID);
          axios.defaults.withCredentials = true;
          axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
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
              console.log(res)
            });
          });
        });
      })();
    },
    addTeacher() {
      let CRContract;
      (async () => {
        // get chain status
        const newWallet = AElf.wallet.createNewWallet();
        CRContract = await this.aelf.chain.contractAt(CRAddress, this.wallet);
        console.log(CRContract);
        var teacherlInfo = {
          teacherID: "10056216001",
          teacherAddress: newWallet.address,
        };
        let formData = new FormData();
        formData.append("teacherID", "10056216001")
        formData.append("teacherName", "张三")
        formData.append("pwd", "10056")
        formData.append("state", "0")
        formData.append("priKey", newWallet.privateKey)
        CRContract.Teacher_Register(teacherlInfo).then((txID) => {
          console.log(txID);
          axios.defaults.withCredentials = true;
          axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
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
              console.log(res)
            });
          });
        });
      })();
    },
    getSchool() {
      let CRContract;
      (async () => {
        // get chain status
        CRContract = await this.aelf.chain.contractAt(CRAddress, this.wallet);
        console.log(CRContract);
        const txRet = await CRContract.get_School.call({
          value: "10056",
        });
        console.log(txRet);
      })();
    },
    getTeacher() {
      let CRContract;
      (async () => {
        // get chain status
        CRContract = await this.aelf.chain.contractAt(CRAddress, this.wallet);
        console.log(CRContract);
        const txRet = await CRContract.get_Teacher.call({
          value: "10056216001",
        });
        console.log(txRet);
      })();
    },
    addCollege() {
      let formData = new FormData();
      formData.append("collegeID", "216")
      formData.append("collegeName", "智能与计算学部")

      axios.defaults.withCredentials = true;
      axios.get("http://127.0.0.1:8000/api/connect").then((res) => {
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
          console.log(res)
        });
      });
    }
  },
};
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
