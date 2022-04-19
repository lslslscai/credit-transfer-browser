from django.http import HttpResponse, JsonResponse
from db_manage.models import getDataFromDB, adjDataToDB, insertDataToDB
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django import forms
from db_manage.form import SRTForm, StuForm, TeaForm
from blockchain_manage.models import cr_handler
# Create your views here.


def searchRes(request):
    if request.method == 'GET':
        print(str(request.GET))
        if request.GET.get('type') == "student":
            if request.GET.get('filter') == "all":
                return getStudent("all")
            else:
                return getStudent(request.GET.get('filter'))
        elif request.GET.get('type') == "school":
            return getSchool(request.GET.get('filter'))
        elif request.GET.get('type') == "college":
            return getCollege(request.GET.get('filter'))
    else:
        return HttpResponse("invalid request!")


def getSchool(flt):
    raw = getDataFromDB("CreditTransferDB", "schoolInfo", {
                        "schoolID": flt}, "one")
    if raw == None:
        return HttpResponse("invalid query!")
    del raw["_id"]
    ret = {}
    ret["school"] = raw["schoolName"]
    print(ret)
    return JsonResponse(ret)


def getCollege(flt):
    raw = getDataFromDB("CreditTransferDB", "collegeInfo", {
                        "collegeID": flt}, "one")
    if raw == None:
        return HttpResponse("invalid query!")
    del raw["_id"]
    ret = {}
    ret["college"] = raw["collegeName"]
    print(ret)
    return JsonResponse(ret)


def getStudent(flt):
    if flt == "all":
        raw = getDataFromDB("CreditTransferDB", "studentInfo", "", "all")
        if raw.__len__() == 0:
            return HttpResponse("invalid query!")
        for i in raw:
            del i["_id"]
        ret = {}
        ret["student"] = raw
        print(ret)
        return JsonResponse(ret)
    else:
        raw = getDataFromDB("CreditTransferDB", "studentInfo", {
                            "studentID": flt}, "one")
        if raw == None:
            return HttpResponse("invalid query!")
        del raw["_id"]
        ret = {}
        ret["student"] = raw
        print(ret)
        return JsonResponse(ret)

def getTeacher(flt):
    raw = getDataFromDB("CreditTransferDB", "teacherInfo", {
                        "teacherID": flt}, "one")
    if raw == None:
        return HttpResponse("invalid query!")
    del raw["_id"]
    ret = {}
    ret["teacher"] = raw
    print(ret)
    return JsonResponse(ret)



def StuRegister(data: dict):
    teacherInfo = getDataFromDB("CreditTransferDB", "teacherInfo",
                        {"teacherID": data["teacherID"]}, "one")
    if teacherInfo == None:
        return HttpResponse("invalid login req!")

    raw = getDataFromDB("CreditTransferDB", "studentInfo",
                        {"studentID": data["studentID"]}, "one")
    if raw != None:
        return HttpResponse("invalid login req!")
    del data["pushType"]
    insertRet = insertDataToDB("CreditTransferDB", "studentInfo", data)

    if insertRet.inserted_id != None:
        handler = cr_handler(teacherInfo["priKey"])
        ret = dict()
        ret["txRet"] = handler.SRT_Create(data)
        return JsonResponse(ret)
    return HttpResponse("register failed!")


def StuLogin(data):
    raw = getDataFromDB("CreditTransferDB", "studentInfo",
                        {"studentID": data["studentID"],
                         "pwd": data["pwd"],
                         "state": 0}, "one"
                        )
    if raw == None:
        return HttpResponse("invalid login req!")
    adjRet = adjDataToDB("CreditTransferDB", "studentInfo",
                         {"studentID": data["studentID"],
                             "pwd": data["pwd"]},
                         {"$set": {"state": 1}},
                         )
    print(adjRet.raw_result)
    res = HttpResponse("login succ!")
    res.set_cookie("Stulogin", data["studentID"], samesite='None', secure=True)
    return res


def StuLogout(data):
    print("logging out!")
    raw = getDataFromDB("CreditTransferDB", "studentInfo",
                        {"studentID": data["studentID"], "state": 1}, "one")
    if raw == None:
        return HttpResponse("already logout!")
    adjRet = adjDataToDB("CreditTransferDB", "studentInfo",
                         {"studentID": data["studentID"]},
                         {"$set": {"state": 0}},
                         )
    print(adjRet.raw_result)
    res = HttpResponse("logout succ!")
    res.delete_cookie("Stulogin", samesite='None')
    return res


def TeaLogin(data):
    raw = getDataFromDB("CreditTransferDB", "teacherInfo",
                        {"teacherID": data["teacherID"],
                         "pwd": data["pwd"],
                         "state": 0}, "one"
                        )
    if raw == None:
        return HttpResponse("invalid login req!")
    adjRet = adjDataToDB("CreditTransferDB", "teacherInfo",
                         {"teacherID": data["teacherID"],
                             "pwd": data["pwd"]},
                         {"$set": {"state": 1}},
                         )
    print(adjRet.raw_result)
    res = HttpResponse("login succ!")
    res.set_cookie("Tealogin", data["teacherID"], samesite='None', secure=True)
    return res


def TeaLogout(data):
    raw = getDataFromDB("CreditTransferDB", "teacherInfo",
                        {"teacherID": data["teacherID"], "state": 1}, "one")
    print(raw.__len__())
    if raw.__len__() == 0:
        return HttpResponse("already logout!")
    adjRet = adjDataToDB("CreditTransferDB", "teacherInfo",
                         {"teacherID": data["teacherID"]},
                         {"$set": {"state": 0}},
                         )
    print(adjRet.raw_result)
    res = HttpResponse("logout succ!")
    res.delete_cookie("Tealogin", samesite='None')
    return res


@csrf_exempt
def adjustReq(request):
    if request.method == 'POST':
        print(str(request.POST))
        if str(request.POST).find("studentID") != -1:
            if str(request.POST).find("Register") != -1:
                form = SRTForm(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    return StuRegister(data)
                else:
                    print(form.errors)
                    return HttpResponse("invalid format")
            form = StuForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(data)
                if data["pushType"] == "Login":
                    return StuLogin(data)
                if data["pushType"] == "Logout":
                    return StuLogout(data)
                return HttpResponse("adf")
            else:
                print(form.errors)
                return HttpResponse("invalid format")
        elif str(request.POST).find("teacherID") != -1:
            form = TeaForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(data)
                if data["pushType"] == "Login":
                    return TeaLogin(data)
                if data["pushType"] == "Logout":
                    return TeaLogout(data)
                return HttpResponse("adf")
            else:
                print(form.errors)
                return HttpResponse("invalid format")
    else:
        return HttpResponse("invalid request!")
