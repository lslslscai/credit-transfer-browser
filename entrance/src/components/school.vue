<template>
  <h1>{{ msg }}</h1>
  <el-button @click="addTeacher">添加教师</el-button>
  <el-form :model="teacherForm">
    <el-form-item label="教师ID" :label-width="width">
      <el-input v-model="teacherForm.teacherID" />
    </el-form-item>
    <el-form-item label="教师名称" :label-width="width">
      <el-input v-model="teacherForm.teacherName" />
    </el-form-item>
    <el-form-item label="密码" :label-width="width">
      <el-input v-model="teacherForm.pwd" />
    </el-form-item>
  </el-form>
  <el-button @click="addCollege">添加学院</el-button>
  <el-form :model="collegeForm">
    <el-form-item label="学院ID" :label-width="width">
      <el-input v-model="collegeForm.collegeID" />
    </el-form-item>
    <el-form-item label="学院名称" :label-width="width">
      <el-input v-model="collegeForm.collegeName" />
    </el-form-item>
  </el-form>
  <br />
  <el-button @click="check">查看学校</el-button>
</template>

<script>
import { ref, reactive } from "vue";
import AElf from "aelf-sdk";
import axios from "axios";
import { useRoute } from "vue-router";

const CRAddress = "2LUmicHyH4RXrMjG4beDwuDsiWJESyLkgkwPdGTR8kahRzq5XS";
export default {
  setup() {
    const count = ref(0);
    const width = "200px";
    const aelf = new AElf(
      new AElf.providers.HttpProvider("http://127.0.0.1:1235")
    );
    const wallet = ref();
    if (!aelf.isConnected()) console.log("Blockchain Node is not running.");
    const r = useRoute();
    console.log(
      "http://127.0.0.1:8000/api/db_admin/select/?type=school&filter=" +
        r.params.id
    );
    axios
      .get(
        "http://127.0.0.1:8000/api/db_admin/select/?type=school&filter=" +
          r.params.id
      )
      .then((res) => {
        console.log(res);
        wallet.value = AElf.wallet.getWalletByPrivateKey(res.data.priKey);
        console.log(wallet);
      });
    const teacherForm = reactive({
      teacherID: "",
      teacherName: "",
      pwd: "",
    });
    const collegeForm = reactive({
      collegeID: "",
      collegeName: "",
    });
    return {
      aelf: aelf,
      wallet: wallet,
      count: count,
      teacherForm: teacherForm,
      collegeForm: collegeForm,
      width: width,
    };
  },
  data() {
    return {};
  },
  methods: {
    check() {
      let CRContract;
      (async () => {
        // get chain status
        const newWallet = AElf.wallet.createNewWallet();
        CRContract = await this.aelf.chain.contractAt(CRAddress, this.wallet);
        console.log(CRContract);
        CRContract.get_School
          .call({ value: this.$route.params.id })
          .then((res) => {
            console.log(res.schoolAddress);
            console.log(this.wallet.address)
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
          teacherID: this.teacherForm.teacherID,
          teacherAddress: newWallet.address,
        };
        let formData = new FormData();
        formData.append("teacherID", this.teacherForm["teacherID"]);
        formData.append("teacherName", this.teacherForm["teacherName"]);
        formData.append("pwd", this.teacherForm.pwd);
        formData.append("state", "0");
        formData.append("priKey", newWallet.privateKey);
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
              console.log(res);
            });
          });
        });
      })();
    },
    addCollege() {
      let formData = new FormData();
      formData.append("collegeID", this.collegeForm["collegeID"]);
      formData.append("collegeName", this.collegeForm["collegeName"]);

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
          console.log(res);
        });
      });
    },
  },
};
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
