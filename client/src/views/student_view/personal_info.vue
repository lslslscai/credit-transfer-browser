<template>
  <el-descriptions
    class="margin-top"
    title="个人信息"
    :column="3"
    size="large"
    border
  >
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <user />
          </el-icon>
          姓名
        </div>
      </template>
      {{name}}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <Iphone />
          </el-icon>
          学号
        </div>
      </template>
      {{ID}}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <location />
          </el-icon>
          在读学历
        </div>
      </template>
      {{type}}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <tickets />
          </el-icon>
          入学年份
        </div>
      </template>
      {{year}}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <office-building />
          </el-icon>
          学校
        </div>
      </template>
      {{school}}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon>
            <office-building />
          </el-icon>
          学院
        </div>
      </template>
      {{college}}
    </el-descriptions-item>
  </el-descriptions>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import {
  Iphone,
  Location,
  OfficeBuilding,
  Tickets,
  User,
} from "@element-plus/icons-vue";
import axios from "axios";
console.log(document.cookie);

const studentID = document.cookie.split("Stulogin=")[1];
const name = ref();
const ID = ref();
const type = ref();
const school = ref();
const college = ref();
const year = ref();
axios
  .get("http://127.0.0.1:8000/api/db_manage/select/?type=student&filter=" + studentID)
  .then((res) => {
      console.log(res)
      name.value = res.data["student"]["studentName"];
      ID.value = res.data["student"]["studentID"];
      type.value = res.data["student"]["type"];
      school.value = res.data["student"]["school"];
      college.value = res.data["student"]["college"];
      year.value = "20"+res.data["student"]["studentID"].substring(7,9);
      console.log(year.value)
  });
</script>

<style scoped>
.el-descriptions {
  margin: 15px auto;
  width: 75%;
}
.cell-item {
  display: flex;
  align-items: center;
  font-size: 16px;
}
.margin-top {
  margin-top: 20px;
}
</style>