<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
import { onMounted } from "vue";

export default {
  name: "App",
  setup() {
    onMounted(() => {
      console.log("in!!!");
      window.onbeforeunload = function (e) {
        e = e || window.event;

        // 兼容IE8和Firefox 4之前的版本
        if (e) {
          e.returnValue = "关闭提示";
        }

        // Chrome, Safari, Firefox 4+, Opera 12+ , IE 9+
        return "关闭提示";
      };
    });
  },
};
</script>
