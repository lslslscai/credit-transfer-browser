<template>
  <div class="score_list">
    <el-table
      :data="tableData"
      height="400"
      style="width: 90%"
    >
      <el-table-column prop="time" label="开课时间" width="180">
      </el-table-column>
      <el-table-column prop="courseID" label="课程ID" width="180">
      </el-table-column>
      <el-table-column prop="courseName" label="课程名称" >
      </el-table-column>
      <el-table-column prop="courseType" label="课程类别" >
      </el-table-column>
      <el-table-column prop="isCompulsory" label="课程性质" >
      </el-table-column>
      <el-table-column prop="credit" label="学分" width="180">
      </el-table-column>
      <el-table-column prop="score" label="成绩" width="180"> </el-table-column>
      <el-table-column prop="GPA" label="绩点" width="180"> </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  props: {
    tableData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
    };
  },
};
</script>
<style scoped>
.el-table {
  margin: 0 auto;
}
</style>