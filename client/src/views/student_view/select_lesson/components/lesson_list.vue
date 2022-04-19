<template>
  <div class="lesson_list">
    <el-table
      :data="tableData"
      height="400"
      style="width: 80%"
      @row-click="select_lesson"
    >
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
  </div>

  <Dialog
    v-bind:data="selectedData"
    :visible="dialogTableVisible"
    :text="text"
    v-on:closeDialog="close_dialog"
  />
</template>

<script>
import Dialog from "../../../../components/dialog/lesson_dialog.vue";
export default {
  props: {
    tableData: {
      type: Array,
      required: true,
    },
  },
  components: {
    Dialog,
  },
  data() {
    return {
      selectedData: [],
      dialogTableVisible: false,
      text: "你确定选这门课吗?"
    };
  },
  methods: {
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },
    select_lesson(row, column, event) {
      this.selectedData.pop();
      this.selectedData.push(row);
      console.log(this.selectedData);
      this.dialogTableVisible = true;
    },
    close_dialog() {
      this.dialogTableVisible = false;
    },
  },
};
</script>
<style scoped>
.el-table {
  margin: 0 auto;
}
</style>