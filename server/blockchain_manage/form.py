from cProfile import label
from django import forms
from django.core.exceptions import ValidationError
from db_manage import form, models

class CourseInfo(forms.Form):
    courseID = forms.CharField(min_length=12, max_length=12, label="课程ID")
    isCompulsory = forms.BooleanField(label="课程性质")
    courseType = forms.IntegerField(max_value=3, label="课程类型")
    isValid = forms.BooleanField(label="课程状态")
    credit = forms.IntegerField(label="学分")

class CourseRecord (forms.Form):
    courseID = forms.CharField(min_length=12, max_length=12, label="课程ID") #course‘s basic info
    studentID = forms.CharField(min_length=15, max_length=15, label="学生ID") #student that have the course
    protocol = forms.JSONField(label="协议") #protocol about the course
    state = forms.BooleanField(label="选课状态") #show course's state (completed, completing, etc.)
    GPA = forms.FloatField(max_value=4.0, label="绩点") #course's credit (float)
    score = forms.FloatField(max_value=100.0, label="分数") #course's score that student gets (float)
    note = forms.CharField(label="补充") #notifications


class Protocol (forms.Form):
    protoID = forms.CharField(label="协议ID")


class SRT (forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15, label="学生ID") #student's ID, it's composed by UID itself and School ID 
    # e.g.: A student has a real ID of 10001, his school's ID is 345. Then his studentID will be 34510001
    rating = forms.IntegerField(label="评分") #shows how actively students participate in the system. (float)
    state = forms.IntegerField(max_value=2, label="学生状态") #show student's state(studying, graduated, retreated)


class School (forms.Form):
    schoolID = forms.CharField(min_length=5, max_length=5, label="学校ID") #school's ID
    schoolAddress = forms.CharField(label="学校地址") #school's blockchain account's address
    rating = forms.IntegerField(label="评分") #shows how actively school and its students participate in the system (float)


class Teacher(forms.Form):
    teacherAddress = forms.CharField(label="学校地址") #教师对应钱包地址
    teacherID = forms.CharField(min_length=11, max_length=11, label="教师ID") #教师编号

#data in process
class SRUploadInput (forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15, label="学生ID") #student that want the course
    courseID = forms.CharField(min_length=12, max_length=12, label="课程ID") #course that to be selected
    protocol = forms.JSONField(label="协议") #protocol about the course
    note = forms.CharField(label="补充") #notification


class SRDropInput(forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15, label="学生ID") #student that have the course
    courseID = forms.CharField(min_length=12, max_length=12, label="课程ID") #course that is selected


class SRModifyInput(forms.Form):
    studentID = forms.CharField(min_length=15, max_length=15, label="学生ID") #student that have the course
    courseID = forms.CharField(min_length=12, max_length=12, label="课程ID") #course that is selected
    state = forms.BooleanField(label="选课状态") #show course's state (completed, completing, etc.)
    GPA = forms.FloatField(max_value=4.0, label="绩点") #course's credit (float)
    score = forms.FloatField(max_value=100.0, label="分数") #course's score that student gets (float)

class courseUpdata(forms.Form):
    schoolID = forms.CharField(min_length=5, max_length=5, label="学校ID") #school's ID
