<template>
  <el-dialog title="提示" v-model="visible" width="50%"  @open="handleOpen">
    <div id="enter">
      <span>{{ text }}</span>
    </div>
    <div id="ret" style="display: none">
      <el-descriptions title="With border" :column="1" size="small" border>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">交易ID</div>
          </template>
          {{ txID }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">交易状态</div>
          </template>
          {{ status }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">交易发起者</div>
          </template>
          {{ from }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">交易函数</div>
          </template>
          {{ method }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">异常信息</div>
          </template>
          {{ err }}
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="check_tx_ret">{{
          btn_text
        }}</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import axios from "axios";
import AElf from "aelf-sdk";
import { ref, reactive } from "vue";
import { useRoute } from "vue-router";
export default {
  emits: ["closeDialog"],
  props: {
    txID: {
      type: String,
      required: true,
    },
    state: {
      type: String,
      required: true,
    },
    visible: {
      type: Boolean,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      status: "",
      method: "",
      from: "",
      btn_text: "检查",
      err: "",
    };
  },
  setup() {
    const checked = ref(false);
    return { checked: checked };
  },
  methods: {
    handleOpen(){
      if(this.$props.state != "db_succ") this.btn_text = "关闭"
    },

    check_tx_ret() {
      if (!this.checked && this.$props.state == "db_succ") {
        const aelf = new AElf(
          new AElf.providers.HttpProvider(
            "http://127.0.0.1:" + this.$route.params.ip
          )
        );
        console.log(this.$props.txID);
        aelf.chain
          .getTxResult(this.$props.txID)
          .then((res) => {
            console.log(res);
            this.status = res["Status"];
            this.method = res["Transaction"]["MethodName"];
            this.from = res["Transaction"]["From"];
            var ret = document.getElementById("ret");
            var enter = document.getElementById("enter");
            ret.setAttribute("style", "display:block");
            enter.setAttribute("style", "display:none");
            this.err = "无";
            if (this.status != "PENDING") {
              this.checked = true;
              this.btn_text = "关闭";
            } else {
              this.btn_text = "重新检查";
            }
          })
          .catch((res) => {
            console.log(res);
            this.status = res["Status"];
            this.method = "invalid";
            this.from = "invalid";
            var ret = document.getElementById("ret");
            var enter = document.getElementById("enter");
            ret.setAttribute("style", "display:block");
            enter.setAttribute("style", "display:none");
            this.checked = true;
            this.btn_text = "关闭";
            this.err = res["Error"];
          });
      }
       else {
        this.$emit("closeDialog");
        this.checked = false;
        var ret = document.getElementById("ret");
        var enter = document.getElementById("enter");
        ret.setAttribute("style", "display:none");
        enter.setAttribute("style", "display:block");
      }
    },
  },
};
</script>
