<template>
  <div class="lesson_list">
    <el-table
      :data="tableData"
      height="400"
      style="width: 80%"
      @row-click="select_lesson"
    >
      <el-table-column prop="studentID" label="学生编号" width="180">
      </el-table-column>
      <el-table-column prop="studentName" label="学生姓名" width="180">
      </el-table-column>
      <el-table-column prop="school" label="学校" >
      </el-table-column>
      <el-table-column prop="college" label="学院" >
      </el-table-column>
      <el-table-column prop="type" label="学历" >
      </el-table-column>
      <el-table-column prop="studentState" label="学生状态" width="180">
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
import Dialog from "../../../../components/dialog/student_dialog.vue";
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
      text: "您可以按需求在下面修改学生信息"
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