from django.http import HttpResponse, JsonResponse
from requests import delete
from db_manage.models import deleteDataFromDB, findAndReplace, getDataFromDB, adjDataToDB, insertDataToDB
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django import forms
from db_admin.form import CollegeForm, CourseRecordForm, SchoolForm, TeaForm, loginForm

# Create your views here.
def SchoolLogin(data):
    print("in!")
    raw = getDataFromDB("CreditTransferDB", "schoolInfo",
                        {"schoolID": data["schoolID"], "pwd": data["schoolPwd"]}, "one")
    if raw == None:
        return HttpResponse("not exist!")
    if data["schoolID"] == "00001":
        return HttpResponse("admin login")
    adjRet = adjDataToDB("CreditTransferDB", "schoolInfo",
                     {"schoolID": data["schoolID"],
                         "pwd": data["schoolPwd"]},
                     {"$set": {"ip": data["blockchainIP"]}},
                     )
    return HttpResponse("login succ!")

def TeaRegister(data):
    raw = getDataFromDB("CreditTransferDB", "teacherInfo",
                        {"teacherID": data["teacherID"]}, "one")

    if data["teacherID"][0:5] != data["sender"]:
        return HttpResponse("sender identification failed!")

    if raw != None:
        return HttpResponse("already registered!")
    del data["sender"]

    insertRet = insertDataToDB("CreditTransferDB", "teacherInfo", data)
    if insertRet.inserted_id != None:
        return HttpResponse("register succ!")
    return HttpResponse("register failed!")


def SchoolRegister(data):
    if data["schoolID"] == "00001":
        return HttpResponse("register succ!")
    raw = getDataFromDB("CreditTransferDB", "schoolInfo",
                        {"schoolID": data["schoolID"]}, "one")
    if raw != None:
        return HttpResponse("already registered!")
    data["ip"] = ""
    insertRet = insertDataToDB("CreditTransferDB", "schoolInfo", data)
    if insertRet.inserted_id != None:
        return HttpResponse("register succ!")
    return HttpResponse("register failed!")


def CollegeCreate(data):
    raw = getDataFromDB("CreditTransferDB", "collegeInfo",
                        {"collegeID": data["collegeID"]}, "one")
    if raw != None:
        return HttpResponse("already registered!")
    insertRet = insertDataToDB("CreditTransferDB", "collegeInfo", data)
    if insertRet.inserted_id != None:
        return HttpResponse("create succ!")
    return HttpResponse("create failed!")


def confirmSelect():
    raw = getDataFromDB("CreditTransferDB", "CRCache", {}, "all")
    if raw.__len__() == 0:
        return HttpResponse("no need to update")
    print(raw)
    for i in raw:
        del i["_id"]
        if i["pushType"] == "SR_Select":
            print("select")
            i["GPA"] = 0
            i["score"] = 0
            i["courseState"] = False
            del i["pushType"]
            insertRet = insertDataToDB("CreditTransferDB", "courseRecord", i)
            dest = getDataFromDB("CreditTransferDB", "courseInfo", 
                                 {"courseID": i["courseID"]}, "one")
            if dest["selected"] < dest["capacity"]:
                dest["selected"] += 1
                replaceRet = findAndReplace("CreditTransferDB", "courseInfo",
                                            {"courseID": i["courseID"]}, dest)
        elif i["pushType"] == "SR_Drop":
            dest = getDataFromDB("CreditTransferDB", "courseInfo", 
                                 {"courseID": i["courseID"]}, "one")
            if dest["selected"] >= 1:
                dest["selected"] -= 1
                replaceRet = findAndReplace("CreditTransferDB", "courseInfo",
                                            {"courseID": i["courseID"]}, dest)
        deleteRet1 = deleteDataFromDB("CreditTransferDB", "CRCache",
                                {"courseID": i["courseID"], "studentID": i["studentID"]})
    return HttpResponse("complete")

# TODO
def TeaAdjust(data):
    raw = getDataFromDB("CreditTransferDB", "teacherInfo",
                        {"teacherID": data["teacherID"]}, "one")
    if raw.__len__() != 0:
        return HttpResponse("already registered!")
    insertRet = insertDataToDB("CreditTransferDB", "teacherInfo", data)
    if insertRet.inserted_id != None:
        return HttpResponse("register succ!")
    return HttpResponse("register failed!")

# TODO


def SchoolAdjust(data):
    raw = getDataFromDB("CreditTransferDB", "schoolInfo",
                        {"schoolID": data["schoolID"]}, "one")
    if raw.__len__() != 0:
        return HttpResponse("already registered!")
    insertRet = insertDataToDB("CreditTransferDB", "schoolInfo", data)
    if insertRet.inserted_id != None:
        return HttpResponse("register succ!")
    return HttpResponse("register failed!")


def getCRCache():
    raw = getDataFromDB("CreditTransferDB", "CRCache", {}, "all")
    keys = []
    for i in raw:
        keys.append(str(i["_id"]))
        del i["_id"]
    ret = dict(zip(keys, raw))
    return JsonResponse(ret)

def getSchool(flt):
    raw = getDataFromDB("CreditTransferDB", "schoolInfo",
                        {"schoolID": flt}, "one")
    if raw != None:
        del raw["_id"]
        ret = {}
        ret["school"] = raw["schoolID"]
        ret["priKey"] = raw["priKey"]
        return JsonResponse(ret)
    return HttpResponse("no data!")

@csrf_exempt
def adjustReq(request):
    try:
        if request.method != 'POST':
            raise Exception("invalid request!")
        print(str(request.POST))
        if str(request.POST).find("SchoolLogin") != -1:
            form = loginForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format")
            data = form.cleaned_data
            print(data)
            return SchoolLogin(data)

        if str(request.POST).find("confirmSelect") != -1:
            print("confirming")
            return confirmSelect()

        elif str(request.POST).find("teacherID") != -1:
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


def searchReq(request):
    try:
        if request.method != 'GET':
            raise Exception("invalid request!")
        if request.GET.get('type') == "courseRecord":
            print("selecting")
            return getCRCache()
        if request.GET.get('type') == "school":
            print("selecting")
            return getSchool(request.GET.get('filter'))
    except Exception as err:
        return HttpResponse(err)
