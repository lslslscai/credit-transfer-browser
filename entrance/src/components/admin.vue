<template>
  <el-button @click="addSchool">添加学校</el-button>
  <el-form :model="schoolForm">
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
</template>

<script>
import { ref, reactive } from "vue";
import AElf from "aelf-sdk";
import axios from "axios";

var url = "mongodb://localhost:27017";
const tokenContractName = "AElf.ContractNames.Token";
const adminPriKey =
  "6fb5eee18c69b147b4f75a0cfc640ea457f69741e7e3c3f07eede7348dba0c9b";
const CRAddress = "2LUmicHyH4RXrMjG4beDwuDsiWJESyLkgkwPdGTR8kahRzq5XS";
export default {
  setup() {
    const width = "200px";
    const aelf = new AElf(
      new AElf.providers.HttpProvider("http://127.0.0.1:1235")
    );
    if (!aelf.isConnected()) console.log("Blockchain Node is not running.");
    const adminWallet = AElf.wallet.getWalletByPrivateKey(adminPriKey);
    const schoolForm = reactive({
      schoolID: "",
      schoolName: "",
      schoolPwd: "",
    });
    let CRContract;
    (async () => {
      // get chain status
      CRContract = await aelf.chain.contractAt(CRAddress, adminWallet);
      console.log(CRContract);
      CRContract.Initialize().then(
        setTimeout((ret) => {
          console.log(ret);
          CRContract.get_AdminAddress.call().then((ret) => {
            console.log(ret);
            var schoolInfo = {
              schoolID: "00001",
              schoolAddress: adminWallet.address,
              rating: 0,
            };
            let formData = new FormData();
            formData.append("schoolID", "00001");
            formData.append("schoolName", "超级管理员");
            formData.append("state", 1);
            axios
              .get(
                "http://127.0.0.1:8000/api/db_admin/select/?type=school&filter=00001"
              )
              .then((res) => {
                console.log(res.data);
                if (res.data == "no data!") {
                  CRContract.School_Register(schoolInfo).then((txID) => {
                    console.log(txID);
                    axios.defaults.withCredentials = true;
                    axios
                      .get("http://127.0.0.1:8000/api/connect")
                      .then((res) => {
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
                }
              });
          });
        }, 5000)
      );
    })();
    return {
      aelf: aelf,
      schoolForm: schoolForm,
      width: width,
      wallet: adminWallet,
    };
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
        const newWallet = AElf.wallet.createNewWallet();
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
              console.log(res);
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
  },
};
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
