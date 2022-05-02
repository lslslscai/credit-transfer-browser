from django import forms
from django.core.exceptions import ValidationError
from db_manage import models

class SRDropInput(forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15, label="学生ID") #student that have the course
    courseID = forms.CharField(min_length=12, max_length=12, label="课程ID") #course that is selected
    pushType = forms.CharField(label="类型")
    
class SRTForm(forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15,label="学生ID")
    studentName = forms.CharField(label="学生姓名")
    type = forms.CharField(label="在读学历")
    school = forms.CharField(label="学校")
    college = forms.CharField(label="学院")
    pwd = forms.CharField(label="密码")
    state = forms.IntegerField(label="状态")
    studentState = forms.CharField(label="学生状态")
    pushType = forms.CharField(label="类型")
    teacherID = forms.CharField(min_length=11, max_length=11, label="教师ID")

class CourseForm(forms.Form):
    courseID = forms.CharField(min_length=12, max_length=12,label="课程ID")
    courseName = forms.CharField(label="课程名称")
    courseType = forms.CharField(label="课程类型")
    school = forms.CharField(label="学校")
    college = forms.CharField(label="学院")
    isCompulsory = forms.BooleanField(label="课程性质")
    isValid = forms.BooleanField(label="开设状态")
    capacity = forms.IntegerField(label="课程容量")
    selected = forms.IntegerField(label="选课人数",required=False)
    pushType = forms.CharField(label="类型")
    teacherID = forms.CharField(min_length=11, max_length=11, label="教师ID")
    credit = forms.FloatField(label="学分")
    protocol = forms.JSONField(label="协议")
class StuForm(forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15,label="学生ID")
    pwd = forms.CharField(label="密码")
    pushType = forms.CharField(label="类型")

class TeaForm(forms.Form):
    teacherID = forms.CharField(min_length=11, max_length=11, label="教师ID")
    pwd = forms.CharField(label="密码")
    pushType = forms.CharField(label="类型")

class CourseRecordForm(forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15,label="学生ID")
    courseID = forms.CharField(min_length=12, max_length=12,label="课程ID")
    protocol = forms.JSONField(label="协议")
    note = forms.CharField(label="备注")
    pushType = forms.CharField(label="类型")

class SRModifyInput(forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15, label="学生ID") #student that have the course
    courseID = forms.CharField(min_length=12, max_length=12, label="课程ID") #course that is selected
    courseState = forms.BooleanField(label="选课状态") #show course's state (completed, completing, etc.)
    GPA = forms.FloatField(max_value=4.0, label="绩点") #course's credit (float)
    score = forms.FloatField(max_value=100.0, label="分数") #course's score that student gets (float)
    pushType = forms.CharField(label="类型")
    teacherID = forms.CharField(min_length=11, max_length=11, label="教师ID")