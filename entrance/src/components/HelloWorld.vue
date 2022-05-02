<template>
  <el-button @click="login">管理员登陆</el-button>
  <el-form :model="adminForm">
    <el-form-item label="地址或ID" :label-width="width">
      <el-input v-model="adminForm.schoolAddress" />
    </el-form-item>
    <el-form-item label="密码" :label-width="width">
      <el-input v-model="adminForm.schoolPwd" />
    </el-form-item>
  </el-form>
</template>

<script>
import { ref, reactive } from "vue";
import {useRouter} from "vue-router";
import AElf from "aelf-sdk";

export default {
  setup() {
    const width = "200px";
    const aelf = new AElf(
      new AElf.providers.HttpProvider("http://127.0.0.1:1235")
    );
    if (!aelf.isConnected()) console.log("Blockchain Node is not running.");
    const adminForm = reactive({
      schoolAddress: "",
      schoolPwd: "",
    });
    return {
      aelf: aelf,
      adminForm: adminForm,
      width: width
    };
  },
  methods: {
    login() {
      console.log(this.aelf.isConnected());
      if (
        this.adminForm.schoolAddress ==
          "2i3sogB66f4RJ5ma19b68Umr6ZhgLA5xgtbwsuhA6fqDr2q8Q4" &&
        this.adminForm.schoolPwd == "c99y10w28"
      ) {
        this.$router.push("/admin")
      } else {
        this.$router.push("/school/"+this.adminForm.schoolAddress)
      }
    }
  },
};
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
