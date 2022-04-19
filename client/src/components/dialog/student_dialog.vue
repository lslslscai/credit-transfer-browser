<template>
  <el-dialog
    title="提示"
    v-model="visible"
    width="60%"
    :before-close="handleClose"
    @open="handleOpen"
  >
    <span>{{ text }}</span>
    <el-form :model="form">
      <el-form-item label="学生编号" :label-width="formLabelWidth">
        <el-input v-model="form.studentID" />
      </el-form-item>
      <el-form-item label="学生姓名" :label-width="formLabelWidth">
        <el-input v-model="form.studentName" />
      </el-form-item>
      <el-form-item label="学生状态" :label-width="formLabelWidth">
        <el-select v-model="form.state" placeholder="Please select a zone">
          <el-option value="在读" />
          <el-option value="毕业" />
          <el-option value="退学" />
        </el-select>
      </el-form-item>
      <el-form-item label="学校" :label-width="formLabelWidth">
        <el-input v-model="form.school" />
      </el-form-item>
      <el-form-item label="学院" :label-width="formLabelWidth">
        <el-input v-model="form.college" />
      </el-form-item>
      <el-form-item label="在读学历" :label-width="formLabelWidth">
        <el-select v-model="form.type" placeholder="Please select a zone">
          <el-option value="本科生" />
          <el-option value="研究生" />
          <el-option value="博士生" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="select_cancel">取 消</el-button>
        <el-button type="primary" @click="select_confirm">确 定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { reactive, ref } from "vue";

export default {
  emits: ["closeDialog"],
  props: {
    data: {
      type: Array,
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
  setup() {
    const formLabelWidth = "140px";
    const form = reactive({
      studentID: "",
      studentName: "",
      state: "",
      school: "",
      college: "",
      type: "",
    });
    return {
      form,
      formLabelWidth,
    };
  },
  data() {
    return {};
  },
  methods: {
    handleOpen() {
      console.log(this.$props.data[0]);
      this.form.studentID = this.$props.data[0]["studentID"];
      this.form.studentName = this.$props.data[0]["studentName"];
      this.form.state = this.$props.data[0]["state"];
      this.form.school = this.$props.data[0]["school"];
      this.form.college = this.$props.data[0]["college"];
      this.form.type = this.$props.data[0]["type"];
    },
    handleClose(done) {
      this.$confirm("确认关闭？将不保存已做的修改")
        .then((_) => {
          this.$emit("closeDialog");
        })
        .catch((_) => {});
    },
    select_confirm() {
      this.$emit("closeDialog");
    },
    select_cancel() {
      this.$confirm("确认关闭？将不保存已做的修改")
        .then((_) => {
          this.$emit("closeDialog");
        })
        .catch((_) => {});
    },
  },
};
</script>

<style scoped>
.el-button--text {
  margin-right: 15px;
}
.el-select {
  width: 300px;
}
.el-input {
  width: 300px;
}
.dialog-footer button:first-child {
  margin-right: 10px;
}
.el-form {
  height: 400px;
  justify-content: left;
}

</style>
