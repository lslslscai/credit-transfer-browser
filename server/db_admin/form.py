from cProfile import label
from django import forms
from django.core.exceptions import ValidationError
from db_manage import models

class SchoolForm(forms.Form):
    schoolID = forms.CharField(min_length=5, max_length=5, label="学校ID")
    schoolName = forms.CharField(label="学校名称")
    priKey = forms.CharField(required=False, label="密钥")
    state = forms.IntegerField(label="类型")
    pwd = forms.CharField(required=False, label="密码")

class CollegeForm(forms.Form):
    collegeID = forms.CharField(min_length=3, max_length=3, label="学院ID")
    collegeName = forms.CharField(label="学院名称")

class TeaForm(forms.Form):
    teacherID = forms.CharField(min_length=11, max_length=11,label="教师ID")
    teacherName = forms.CharField(label="教师姓名")
    pwd = forms.CharField(label="密码")
    state = forms.IntegerField(label="类型")
    priKey = forms.CharField(label="密钥")

class CourseRecordForm(forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15,label="学生ID")
    courseID = forms.CharField(min_length=12, max_length=12,label="课程ID")
    protocol = forms.JSONField(label="协议")
    note = forms.CharField(label="备注")
    GPA = forms.FloatField(max_value=4, label="绩点")
    score = forms.FloatField(max_value=100, label="成绩")
    courseState = forms.BooleanField(label="状态")