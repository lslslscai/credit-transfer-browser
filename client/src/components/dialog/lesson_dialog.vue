<template>
  <el-dialog
    title="提示"
    v-model="visible"
    width="50%"
    :before-close="handleClose"
  >
    <span>{{ text }}</span>
    <el-table :data="data">
      <el-table-column prop="courseID" label="课程ID" width="180">
      </el-table-column>
      <el-table-column prop="courseName" label="课程名称"> </el-table-column>
      <el-table-column prop="school" label="所属学校" width="180">
      </el-table-column>
      <el-table-column prop="college" label="开课学院" width="180">
      </el-table-column>
      <el-table-column prop="capacity" label="课程容量" width="180">
      </el-table-column>
      <el-table-column prop="selected" label="已选课" width="180">
      </el-table-column>
    </el-table>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="select_confirm">取 消</el-button>
        <el-button type="primary" @click="select_cancel">确 定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
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
  data() {
    return {};
  },
  methods: {
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },
    select_confirm() {
      this.$emit("closeDialog");
    },
    select_cancel() {
      this.$emit("closeDialog");
    },
  },
};
</script>
