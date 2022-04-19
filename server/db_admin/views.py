from django.http import HttpResponse, JsonResponse
from db_manage.models import getDataFromDB, adjDataToDB, insertDataToDB
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django import forms
from db_admin.form import CollegeForm, SchoolForm, TeaForm

# Create your views here.

def TeaRegister(data):
    raw = getDataFromDB("CreditTransferDB", "teacherInfo",
                        {"teacherID": data["teacherID"]}, "one")
    if raw != None:
        return HttpResponse("already registered!")
    insertRet = insertDataToDB("CreditTransferDB", "teacherInfo", data)
    if insertRet.inserted_id != None:
        return HttpResponse("register succ!")
    return HttpResponse("register failed!")

def SchoolRegister(data):
    raw = getDataFromDB("CreditTransferDB", "schoolInfo",
                        {"schoolID": data["schoolID"]}, "one")
    if raw != None:
        return HttpResponse("already registered!")
    insertRet = insertDataToDB("CreditTransferDB", "schoolInfo", data)
    if insertRet.inserted_id != None:
        return HttpResponse("register succ!")
    return HttpResponse("register failed!")

def CollegeCreate(data):
    raw = getDataFromDB("CreditTransferDB", "collegelInfo",
                        {"collegeID": data["collegeID"]}, "one")
    if raw != None:
        return HttpResponse("already registered!")
    insertRet = insertDataToDB("CreditTransferDB", "collegeInfo", data)
    if insertRet.inserted_id != None:
        return HttpResponse("create succ!")
    return HttpResponse("create failed!")
# TODO
def TeaAdjust(data):
    raw = getDataFromDB("CreditTransferDB", "teacherInfo",
                        {"teacherID": data["teacherID"]})
    if raw.__len__() != 0:
        return HttpResponse("already registered!")
    insertRet = insertDataToDB("CreditTransferDB", "teacherInfo", data)
    if insertRet.inserted_id != None:
        return HttpResponse("register succ!")
    return HttpResponse("register failed!")

# TODO
def SchoolAdjust(data):
    raw = getDataFromDB("CreditTransferDB", "schoolInfo",
                        {"schoolID": data["schoolID"]})
    if raw.__len__() != 0:
        return HttpResponse("already registered!")
    insertRet = insertDataToDB("CreditTransferDB", "schoolInfo", data)
    if insertRet.inserted_id != None:
        return HttpResponse("register succ!")
    return HttpResponse("register failed!")



@csrf_exempt
def adjustReq(request):
    try:
        if request.method != 'POST':
            raise Exception("invalid request!")
        print(str(request.POST))
        if str(request.POST).find("teacherID") != -1:
            form = TeaForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format")
            data = form.cleaned_data
            print(data)
            return TeaRegister(data)

        elif str(request.POST).find("schoolID") != -1:
            form = SchoolForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format")
            data = form.cleaned_data
            print(data)
            return SchoolRegister(data)

        elif str(request.POST).find("collegeID") != -1:
            form = CollegeForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format")
            data = form.cleaned_data
            print(data)
            return CollegeCreate(data)
    except Exception as err:
        return HttpResponse(err)

