<template>
  <div class="loading">加载中</div>
  <div class="content" hidden="hidden">
    <el-button @click="addSchool">添加学校</el-button>
    <el-form :model="schoolForm">
      <el-form-item label="学校钱包密钥" :label-width="width">
        <el-input v-model="schoolForm.schoolPriKey" />
      </el-form-item>
      <el-form-item label="学校ID" :label-width="width">
        <el-input v-model="schoolForm.schoolID" />
      </el-form-item>
      <el-form-item label="学校名称" :label-width="width">
        <el-input v-model="schoolForm.schoolName" />
      </el-form-item>
      <el-form-item label="密码" :label-width="width">
        <el-input v-model="schoolForm.schoolPwd" />
      </el-form-item>
    </el-form>
    <el-button @click="confirmSelect">确认选课</el-button>
    <el-button @click="testApproveAndTransfer">测试1</el-button>
  </div>

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
const tokenContractName = "AElf.ContractNames.Token";
const CRAddress = "2LUmicHyH4RXrMjG4beDwuDsiWJESyLkgkwPdGTR8kahRzq5XS";
export default {
  setup() {
    const width = "200px";
    const r = useRoute();
    const aelf = new AElf(
      new AElf.providers.HttpProvider("http://127.0.0.1:" + r.params.ip)
    );
    if (!aelf.isConnected()) console.log("Blockchain Node is not running.");
    const schoolForm = reactive({
      schoolID: "",
      schoolName: "",
      schoolPwd: "",
      schoolPriKey: "",
    });
    const adminWallet = ref();
    axios
      .get(
        "http://127.0.0.1:8000/api/db_admin/select/?type=school&filter=00001"
      )
      .then((res) => {
        let wallet = AElf.wallet.getWalletByPrivateKey(res.data.priKey);
        let CRContract;
        (async () => {
          // get chain status
          CRContract = await aelf.chain.contractAt(CRAddress, wallet);
          CRContract.Initialize().then(
            setTimeout(() => {
              var schoolInfo = {
                schoolID: "00001",
                schoolAddress: wallet.address,
                rating: 0,
              };
              CRContract.School_Register(schoolInfo).then((txID) => {
                adminWallet.value = wallet;
                alert("超级管理员初始化成功！");
                var loadingModule =
                  document.getElementsByClassName("loading")[0];
                var mainModule = document.getElementsByClassName("content")[0];
                loadingModule.setAttribute("style", "display:none");
                mainModule.removeAttribute("hidden");
              });
            }, 5000)
          );
        })();
      });

    return {
      aelf: aelf,
      schoolForm: schoolForm,
      width: width,
      wallet: adminWallet,
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
    testApproveAndTransfer() {
      console.log(this.wallet);
      let tokenContractAddress;
      let tokenContract;
      (async () => {
        // get chain status
        const chainStatus = await this.aelf.chain.getChainStatus();
        // get genesis contract address
        const GenesisContractAddress = chainStatus.GenesisContractAddress;
        // get genesis contract instance
        const zeroContract = await this.aelf.chain.contractAt(
          GenesisContractAddress,
          this.wallet
        );
        // Get contract address by the read only method `GetContractAddressByName` of genesis contract
        tokenContractAddress = await zeroContract.GetContractAddressByName.call(
          AElf.utils.sha256(tokenContractName)
        );

        tokenContract = await this.aelf.chain.contractAt(
          tokenContractAddress,
          this.wallet
        );

        tokenContract.GetBalance.call({
          owner: "2i3sogB66f4RJ5ma19b68Umr6ZhgLA5xgtbwsuhA6fqDr2q8Q4",
          symbol: "ELF",
        }).then((res) => {
          console.log(res);
          tokenContract
            .Approve({
              spender: CRAddress,
              symbol: "ELF",
              amount: res.balance,
            })
            .then((res) => {
              console.log(res);
              tokenContract.GetAllowance.call({
                spender: CRAddress,
                symbol: "ELF",
                owner: this.wallet.address,
              }).then((res) => {
                console.log(res);
              });
            });
        });
      })();
    },

    addSchool() {
      let CRContract;
      (async () => {
        // get chain status
        CRContract = await this.aelf.chain.contractAt(CRAddress, this.wallet);
        const newWallet = AElf.wallet.getWalletByPrivateKey(
          this.schoolForm.schoolPriKey
        );
        console.log(CRContract);
        var schoolInfo = {
          schoolID: this.schoolForm["schoolID"],
          schoolAddress: newWallet.address,
          rating: 0,
        };
        let formData = new FormData();
        formData.append("schoolID", this.schoolForm["schoolID"]);
        formData.append("schoolName", this.schoolForm["schoolName"]);
        formData.append("priKey", newWallet.privateKey);
        formData.append("state", 0);
        formData.append("pwd", this.schoolForm.schoolPwd);
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
              CRContract.School_Register(schoolInfo).then((txID) => {
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
    confirmSelect() {
      let CRContract;
      let formData = new FormData();
      formData.append("schoolID", "10056");
      axios
        .get("http://127.0.0.1:8000/api/db_admin/select/?type=courseRecord")
        .then((res) => {
          console.log(res.data);
          let content = res.data;
          (async () => {
            // get chain status
            CRContract = await this.aelf.chain.contractAt(
              CRAddress,
              this.wallet
            );
            for (var item in content) {
              if (res.data[item]["pushType"] == "SR_Select") {
                console.log(res.data[item]["pushType"]);
                var courseRecord = {
                  courseID: res.data[item]["courseID"],
                  studentID: res.data[item]["studentID"],
                  protocol: {
                    startDate: res.data[item]["protocol"].startDate,
                    testDate: res.data[item]["protocol"].testDate,
                    projectDate: res.data[item]["protocol"].projectDate,
                    rateOfProject: res.data[item]["protocol"].rateOfProject,
                    rateOfTest: res.data[item]["protocol"].rateOfTest,
                  },
                  note: res.data[item]["note"],
                };

                console.log(courseRecord);
                CRContract.SR_Select(courseRecord).then((txID) => {
                  console.log(txID);
                });
              } else if (res.data[item]["pushType"] == "SR_Drop") {
                var courseRecord = {
                  courseID: res.data[item]["courseID"],
                  studentID: res.data[item]["studentID"],
                };
                console.log(courseRecord);
                CRContract.SR_Drop(courseRecord).then((txID) => {
                  console.log(txID);
                });
              }
            }
          })().then(() => {
            let formData = new FormData();
            formData.append("pushType", "confirmSelect");
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
.loading {
  color: rgb(162, 162, 162);
  margin-top: 5rem;
  font-size: 2rem;
}
</style>
