from django import forms
from django.core.exceptions import ValidationError
from db_manage import models

class SRTForm(forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15,label="学生ID")
    studentName = forms.CharField(label="学生姓名")
    type = forms.CharField(label="在读学历")
    school = forms.CharField(label="学校")
    college = forms.CharField(label="学院")
    pwd = forms.CharField(label="密码")
    state = forms.IntegerField(label="状态")
    pushType = forms.CharField(label="类型")
    teacherID = forms.CharField(min_length=11, max_length=11, label="教师ID")

class StuForm(forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15,label="学生ID")
    pwd = forms.CharField(label="密码")
    pushType = forms.CharField(label="类型")

class TeaForm(forms.Form):
    teacherID = forms.CharField(min_length=11, max_length=11, label="教师ID")
    pwd = forms.CharField(label="密码")
    pushType = forms.CharField(label="类型")