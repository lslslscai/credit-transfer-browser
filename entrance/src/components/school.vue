<template>
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

  <Dialog
    v-bind:visible="dialogTableVisible"
    :txID="txID"
    :text="result"
    :state="state"
    v-on:closeDialog="close_dialog"
  />
</template>

<script>
import { ref, reactive } from "vue";
import AElf from "aelf-sdk";
import axios from "axios";
import { useRoute } from "vue-router";
import Dialog from "./result.vue";
const CRAddress = "2LUmicHyH4RXrMjG4beDwuDsiWJESyLkgkwPdGTR8kahRzq5XS";
export default {
  setup() {
    const count = ref(0);
    const width = "200px";
    const r = useRoute();
    console.log(r.params);
    const aelf = new AElf(
      new AElf.providers.HttpProvider("http://127.0.0.1:" + r.params.ip)
    );
    const wallet = ref();
    if (!aelf.isConnected()) console.log("Blockchain Node is not running.");
    axios
      .get(
        "http://127.0.0.1:8000/api/db_admin/select/?type=school&filter=" +
          r.params.id
      )
      .then((res) => {
        console.log(res);
        let w = AElf.wallet.getWalletByPrivateKey(res.data.priKey);
        wallet.value = w;
      });
    const teacherForm = reactive({
      teacherID: "10001001001",
      teacherName: "张三",
      pwd: "",
    });
    const collegeForm = reactive({
      collegeID: "001",
      collegeName: "计算机学院",
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
    return {
      dialogTableVisible: false,
      txID: "",
      result: "",
      state: "",
    };
  },
  components: {
    Dialog,
  },
  methods: {
    addTeacher() {
      let CRContract;
      (async () => {
        // get chain status
        const newWallet = AElf.wallet.createNewWallet();
        console.log(this.wallet);
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
        formData.append("sender", this.$route.params.id);
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
            if (res.data == "register succ!") {
              CRContract.Teacher_Register(teacherlInfo).then((txID) => {
                this.txID = txID["TransactionId"];
                console.log(this.txID);
                this.result = "数据库完成修改！请检查区块链交易结果";
                this.dialogTableVisible = true;
                this.state = "db_succ";
              });
            } else {
              this.result = "数据库失败！" + res.data;
              this.dialogTableVisible = true;
              this.state = "db_fail";
            }
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
          if (res.data == "create succ!") {
            this.txID = "";
            this.result = "数据库完成修改！";
            this.dialogTableVisible = true;
            this.state = "no_tran";
          } else {
            this.result = "数据库失败！" + res.data;
            this.dialogTableVisible = true;
            this.state = "db_fail";
          }
        });
      });
    },
    close_dialog() {
      this.dialogTableVisible = false;
    },
  },
};
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
