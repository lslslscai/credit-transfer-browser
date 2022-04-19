from django import forms
from django.core.exceptions import ValidationError
from db_manage import models

class SchoolForm(forms.Form):
    schoolID = forms.CharField(min_length=5, max_length=5, label="学校ID")
    schoolName = forms.CharField(label="学校名称")

class CollegeForm(forms.Form):
    collegeID = forms.CharField(min_length=3, max_length=3, label="学院ID")
    collegeName = forms.CharField(label="学院名称")

class TeaForm(forms.Form):
    teacherID = forms.CharField(min_length=11, max_length=11,label="教师ID")
    teacherName = forms.CharField(label="教师姓名")
    pwd = forms.CharField(label="密码")
    state = forms.IntegerField(label="类型")
    priKey = forms.CharField(label="密钥")