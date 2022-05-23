import traceback
from django.http import HttpResponse, JsonResponse
from db_manage.models import deleteDataFromDB, findAndReplace, getDataFromDB, adjDataToDB, insertDataToDB
from django.views.decorators.csrf import csrf_exempt
from db_manage.form import SRTForm, StuForm, TeaForm, CourseForm, CourseRecordForm, SRModifyInput, SRDropInput
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
        elif request.GET.get('type') == "course":
            return getCourseInfo(request.GET.get('filter'))
        elif request.GET.get('type') == "courseRecord":
            return getCourseRecord(request.GET.get('filter'), request.GET.get("value"))
        elif request.GET.get('type') == "CRCache":
            return getCRCache(request.GET.get('filter'))
        elif request.GET.get('type') == "txRet":
            return getTransactionRet(request.GET.get('teacherID'), request.GET.get('txID'))
    else:
        return HttpResponse("invalid request!")


def getSchool(flt):
    if flt == "all":
        raw = getDataFromDB("CreditTransferDB", "schoolInfo", {"schoolID":{"$nin": ["00001"]}}, "all")
        if raw.__len__() == 0:
            return HttpResponse("invalid query!")
        for i in raw:
            del i["_id"]
        ret = {}
        ret["school"] = raw
        print(ret)
        return JsonResponse(ret)
    else:
        raw = getDataFromDB("CreditTransferDB", "schoolInfo", {
                            "schoolID": flt}, "one")
        if raw == None:
            return HttpResponse("invalid query!")
        del raw["_id"]
        ret = {}
        ret["school"] = raw["schoolName"]
        print(ret)
        return JsonResponse(ret)


def getCRCache(flt):
    raw = getDataFromDB("CreditTransferDB", "CRCache",
                        {"studentID": flt}, "all")
    ret = {}
    for i in raw:
        del i["_id"]
    ret["record"] = raw
    print(ret)
    return JsonResponse(ret)


def getCourseRecord(flt, value):
    if flt == "student":
        raw = getDataFromDB("CreditTransferDB", "courseRecord", {
            "studentID": value}, "all")
    elif flt == "courseNotFinish":
        raw = getDataFromDB("CreditTransferDB", "courseRecord", {
            "courseID": value, "courseState": False}, "all")
    else:
        raw = getDataFromDB("CreditTransferDB", "courseRecord", {
            "courseID": value}, "all")
    ret = {}
    if raw.__len__() != 0:
        for i in raw:
            del i["_id"]
    ret["record"] = raw
    print(ret)
    return JsonResponse(ret)


def getCollege(flt):
    if flt == "all":
        raw = getDataFromDB("CreditTransferDB", "collegeInfo", {}, "all")
        if raw.__len__() == 0:
            return HttpResponse("invalid query!")
        for i in raw:
            del i["_id"]
        ret = {}
        ret["college"] = raw
        print(ret)
        return JsonResponse(ret)
    else:
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
    if flt == "all" or flt.find('^') != -1:
        if flt.find('^') != -1:
            print("in")
            raw = getDataFromDB("CreditTransferDB", "studentInfo", {
                "studentID": {"$regex": flt}}, "all")
        else:
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


def getCourseInfo(flt: str):
    if flt == "all" or flt.find('^') != -1:
        if flt.find('^') != -1:
            print("in")
            raw = getDataFromDB("CreditTransferDB", "courseInfo", {
                "courseID": {"$regex": flt}}, "all")
        else:
            raw = getDataFromDB("CreditTransferDB", "courseInfo", "", "all")
        print(raw)
        if raw.__len__() == 0:
            return HttpResponse("invalid query!")
        for i in raw:
            del i["_id"]
        ret = {}
        ret["course"] = raw
        print(ret)
        return JsonResponse(ret)
    else:
        raw = getDataFromDB("CreditTransferDB", "courseInfo", {
                            "courseID": flt}, "one")
        if raw == None:
            return HttpResponse("invalid query!")
        del raw["_id"]
        ret = {}
        ret["course"] = raw
        print(ret)
        return JsonResponse(ret)


def getTransactionRet(teacherID, txID):
    teacherInfo = getDataFromDB("CreditTransferDB", "teacherInfo",
                                {"teacherID": teacherID}, "one")
    schoolInfo = getDataFromDB("CreditTransferDB", "schoolInfo",
                               {"schoolID": teacherID[0:5]}, "one")
    handler = cr_handler(teacherInfo["priKey"], schoolInfo["ip"])
    print("checking")
    ret = dict()
    ret = handler.getTransactionResult(txID)
    return JsonResponse(ret)


def StuRegister(data: dict):
    teacherInfo = getDataFromDB("CreditTransferDB", "teacherInfo",
                                {"teacherID": data["teacherID"]}, "one")
    schoolInfo = getDataFromDB("CreditTransferDB", "schoolInfo",
                               {"schoolID": data["teacherID"][0:5]}, "one")
    if teacherInfo == None or schoolInfo == None:
        return HttpResponse("sender identification error!")

    raw = getDataFromDB("CreditTransferDB", "studentInfo",
                        {"studentID": data["studentID"]}, "one")
    if raw != None:
        return HttpResponse("already registered!")
    del data["pushType"]
    del data["teacherID"]
    data["studentState"] = "在读"
    insertRet = insertDataToDB("CreditTransferDB", "studentInfo", data)

    if insertRet.inserted_id != None:
        handler = cr_handler(teacherInfo["priKey"], schoolInfo["ip"])
        ret = dict()
        ret["txRet"] = handler.SRT_Create(data)
        return JsonResponse(ret)
    return HttpResponse("register failed!")


def CourseCreate(data: dict):
    teacherInfo = getDataFromDB("CreditTransferDB", "teacherInfo",
                                {"teacherID": data["teacherID"]}, "one")
    schoolInfo = getDataFromDB("CreditTransferDB", "schoolInfo",
                               {"schoolID": data["teacherID"][0:5]}, "one")
    if teacherInfo == None or schoolInfo == None:
        return HttpResponse("sender identification error!")

    raw = getDataFromDB("CreditTransferDB", "courseInfo",
                        {"courseID": data["courseID"]}, "one")
    if raw != None:
        return HttpResponse("already created!")
    del data["pushType"]
    del data["teacherID"]

    data["selected"] = 0
    insertRet = insertDataToDB("CreditTransferDB", "courseInfo", data)

    if insertRet.inserted_id != None:
        if data["courseType"] == "课内课程":
            data["courseType"] = 0
        elif data["courseType"] == "校内跨专业课程":
            data["courseType"] = 1
        elif data["courseType"] == "跨校课程":
            data["courseType"] = 2
        elif data["courseType"] == "课外课程":
            data["courseType"] = 3
        data["credit"] = int(data["credit"] * 100)
        print(data)
        handler = cr_handler(teacherInfo["priKey"], schoolInfo["ip"])
        ret = dict()
        ret["txRet"] = handler.Course_Create(data)
        return JsonResponse(ret)
    return HttpResponse("create failed!")


def CourseModify(data: dict):
    teacherInfo = getDataFromDB("CreditTransferDB", "teacherInfo",
                                {"teacherID": data["teacherID"]}, "one")
    schoolInfo = getDataFromDB("CreditTransferDB", "schoolInfo",
                               {"schoolID": data["teacherID"][0:5]}, "one")
    if teacherInfo == None or schoolInfo == None:
        return HttpResponse("sender identification error!")
    raw = getDataFromDB("CreditTransferDB", "courseInfo",
                        {"courseID": data["courseID"]}, "one")
    if raw == None:
        return HttpResponse("invalid req!")
    del data["pushType"]
    del data["teacherID"]
    adjRet = findAndReplace("CreditTransferDB", "courseInfo", {
                            "courseID": data["courseID"]}, data)

    if adjRet != None:
        handler = cr_handler(teacherInfo["priKey"], schoolInfo["ip"])
        if data["courseType"] == "课内课程":
            data["courseType"] = 0
        elif data["courseType"] == "校内跨专业课程":
            data["courseType"] = 1
        elif data["courseType"] == "跨校课程":
            data["courseType"] = 2
        elif data["courseType"] == "课外课程":
            data["courseType"] = 3
        data["credit"] = int(data["credit"] * 100)
        ret = dict()
        print(data)
        ret["txRet"] = handler.Course_Adjust(data)
        return JsonResponse(ret)
    return HttpResponse("register failed!")


def StuAdjust(data: dict):
    teacherInfo = getDataFromDB("CreditTransferDB", "teacherInfo",
                                {"teacherID": data["teacherID"]}, "one")
    schoolInfo = getDataFromDB("CreditTransferDB", "schoolInfo",
                               {"schoolID": data["teacherID"][0:5]}, "one")
    if teacherInfo == None or schoolInfo == None:
        return HttpResponse("sender identification error!")
    raw = getDataFromDB("CreditTransferDB", "studentInfo",
                        {"studentID": data["studentID"]}, "one")
    if raw == None:
        return HttpResponse("invalid req!")
    del data["pushType"]
    del data["teacherID"]
    print(data)
    adjRet = findAndReplace("CreditTransferDB", "studentInfo", {
                            "studentID": data["studentID"]}, data)

    if adjRet != None:
        handler = cr_handler(teacherInfo["priKey"], schoolInfo["ip"])
        if data["studentState"] == "在读":
            data["studentState"] = 0
        if data["studentState"] == "毕业":
            data["studentState"] = 1
        if data["studentState"] == "退学":
            data["studentState"] = 2

        ret = dict()
        ret["txRet"] = handler.SRT_Adjust(data)
        return JsonResponse(ret)
    return HttpResponse("register failed!")


def SRSelect(data: dict):
    raw1 = getDataFromDB("CreditTransferDB", "CRCache",
                         {"courseID": data["courseID"],
                          "studentID": data["studentID"],
                          "pushType": data["pushType"]}, "one")
    raw2 = getDataFromDB("CreditTransferDB", "courseRecord",
                         {"courseID": data["courseID"], "studentID": data["studentID"]}, "one")
    if raw1 != None or raw2 != None:
        return HttpResponse("already selected!")
    raw = getDataFromDB("CreditTransferDB", "studentInfo",
                        {"studentID": data["studentID"], "state": 1}, "one")
    
    if raw == None:
        return HttpResponse("invalid sender!")
    raw = getDataFromDB("CreditTransferDB", "courseInfo",
                        {"courseID": data["courseID"]}, "one")
    print("course"+str(raw))
    if raw == None:
        return HttpResponse("invalid courseID!")
    if raw["selected"] >= raw["capacity"]:
        return HttpResponse("already full capacity!")

    insertRet = insertDataToDB("CreditTransferDB", "CRCache", data)
    print(insertRet.inserted_id)
    res = HttpResponse("select succ!")
    return res


def SRAdjust(data: dict):
    print(data)
    raw = getDataFromDB("CreditTransferDB", "courseRecord",
                        {"courseID": data["courseID"], "studentID": data["studentID"]}, "one")
    if raw == None:
        return HttpResponse("not exist!")
    if raw["courseState"] == True:
        return HttpResponse("can't modify!")

    teacherInfo = getDataFromDB("CreditTransferDB", "teacherInfo",
                                {"teacherID": data["teacherID"]}, "one")
    schoolInfo = getDataFromDB("CreditTransferDB", "schoolInfo",
                               {"schoolID": data["courseID"][0:5]}, "one")
    if teacherInfo == None or schoolInfo == None or \
        data["teacherID"][0:5] != data["courseID"][0:5]:
        return HttpResponse("sender identification error!")

    if data["score"] != 0 and not data["courseState"]:
        return HttpResponse("invalid courseState!")
    adjRet = adjDataToDB("CreditTransferDB", "courseRecord",
                         {"studentID": data["studentID"],
                             "courseID": data["courseID"]},
                         {"$set": {"score": data["score"], "GPA": data["GPA"], "courseState": data["courseState"]}})
    print(adjRet)
    if adjRet != None:
        handler = cr_handler(teacherInfo["priKey"], schoolInfo["ip"])

        ret = dict()
        ret["txRet"] = handler.SR_Adjust(data)
        return JsonResponse(ret)
    res = HttpResponse("modify succ!")
    return res


def SRDrop(data: dict):
    print(data)
    raw = getDataFromDB("CreditTransferDB", "CRCache",
                        {"courseID": data["courseID"], "studentID": data["studentID"]}, "one")
    if raw != None:
        delRet = deleteDataFromDB("CreditTransferDB", "CRCache",
                                  {"courseID": data["courseID"], "studentID": data["studentID"]})
        return HttpResponse("drop succ!")

    raw = getDataFromDB("CreditTransferDB", "courseRecord",
                        {"courseID": data["courseID"], "studentID": data["studentID"]}, "one")
    if raw == None:
        return HttpResponse("already droped!")

    insertRet = insertDataToDB("CreditTransferDB", "CRCache", data)
    deleteRet = deleteDataFromDB("CreditTransferDB", "courseRecord",
                                 {"courseID": data["courseID"], "studentID": data["studentID"]})
    print(insertRet.inserted_id)
    res = HttpResponse("drop succ!")
    return res


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

    if raw == None:
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
    try:
        if request.method != 'POST':
            raise Exception("invalid request!")
        print(str(request.POST))
        # student
        if str(request.POST).find("SRT_Register") != -1:
            form = SRTForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format!")
            data = form.cleaned_data
            return StuRegister(data)
        elif str(request.POST).find("SRT_Adjust") != -1:
            form = SRTForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format!")
            data = form.cleaned_data
            return StuAdjust(data)
        elif str(request.POST).find("Stu_Login") != -1:
            form = StuForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format!")
            data = form.cleaned_data
            return StuLogin(data)
        elif str(request.POST).find("Stu_Logout") != -1:
            form = StuForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format!")
            data = form.cleaned_data
            return StuLogout(data)
        # Teacher
        elif str(request.POST).find("Tea_Login") != -1:
            form = TeaForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format!")
            data = form.cleaned_data
            return TeaLogin(data)
        elif str(request.POST).find("Tea_Logout") != -1:
            form = TeaForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format!")
            data = form.cleaned_data
            return TeaLogout(data)
        # course
        elif str(request.POST).find("Course_Create") != -1:
            form = CourseForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format!" + form.errors.__str__())
            data = form.cleaned_data
            return CourseCreate(data)
        elif str(request.POST).find("Course_Modify") != -1:
            form = CourseForm(request.POST)
            if not form.is_valid():
                print(form.errors)
                raise Exception("invalid format!")
            data = form.cleaned_data
            return CourseModify(data)
        # courseRecord
        elif str(request.POST).find("SR_Select") != -1:
            form = CourseRecordForm(request.POST)
            if not form.is_valid():
                raise Exception("invalid format!")
            data = form.cleaned_data
            return SRSelect(data)
        elif str(request.POST).find("SR_Adjust") != -1:
            form = SRModifyInput(request.POST)
            if not form.is_valid():
                print(form.errors.__str__())
                raise Exception("invalid format!")
            data = form.cleaned_data
            return SRAdjust(data)
        elif str(request.POST).find("SR_Drop") != -1:
            form = SRDropInput(request.POST)
            if not form.is_valid():
                raise Exception("invalid format!")
            data = form.cleaned_data
            return SRDrop(data)
        raise Exception("invalid push type")
    except Exception as err:
        print(err)
        return HttpResponse(err)
