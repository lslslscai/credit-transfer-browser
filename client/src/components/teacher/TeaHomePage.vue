<template>
  <div>
    <Navigate />
    <router-view></router-view>
  </div>
</template>

<script>
import Navigate from "./TeaNavigate.vue";

export default {
  name: "App",
  components: {
    Navigate,
  },
};
</script>
