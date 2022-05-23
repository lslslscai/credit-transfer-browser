from django.shortcuts import render
from blockchain_manage.models import cr_handler
from django.http import HttpResponse, JsonResponse
from blockchain_manage.form import SRT, CourseInfo
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

def resolve_req(req):
    if req.method == 'POST':
        print("content:"+str(req.POST))
        if str(req.path).find("SRT_Create") != -1:
            print ("creating a SRT")
            form = SRT(req.POST)
            if form.is_valid():
                return form.cleaned_data
            raise Exception("invalid SRT input", form.errors)
        elif str(req.path).find("Course_Create") != -1:
            print ("creating a Course")
            form = CourseInfo(req.POST)
            if form.is_valid():
                return form.cleaned_data
            raise Exception("invalid SRT input", form.errors)
    elif req.method == 'GET':
        if str(req.path).find("get_Ret") != -1:
            print("getting txRet")
            if req.GET.get("txID", "0") != "0":
                return req.GET.get("txID")
            raise Exception("invalid txID")
        elif str(req.path).find("get_SRT") != -1:
            print("getting SRT")
            if req.GET.get("studentID", "0") != "0":
                return req.GET.get("studentID")
            raise Exception("invalid SRT req")
        elif str(req.path).find("get_School") != -1:
            print("getting School")
            if req.GET.get("schoolID", "0") != "0":
                return req.GET.get("schoolID")
            raise Exception("invalid School req")

    else: raise Exception("invalid req type!")

@csrf_exempt
def SRT_Create(req):
    try:
        data = resolve_req(req)
        print(data)
        priKey = data["priKey"]
        ip = data["ip"]
        handler = cr_handler(priKey, ip)
        ret = dict()
        ret["txRet"] = handler.SRT_Create(data)
        return JsonResponse(ret)
    except Exception as err:
        print(err)
        return HttpResponse(err)

def get_SRT(req):
    try:
        data = resolve_req(req)
        priKey = data["priKey"]
        ip = data["ip"]
        handler = cr_handler(priKey, ip)
        ret = handler.get_SRT(data)
        return JsonResponse(ret)
    except Exception as err:
        print(err)
        return HttpResponse(err)

def get_School(req):
    try:
        data = resolve_req(req)
        priKey = data["priKey"]
        ip = data["ip"]
        handler = cr_handler(priKey, ip)
        ret = handler.get_School(data)
        return JsonResponse(ret)
    except Exception as err:
        print(err)
        return HttpResponse(err)

def get_ret(req):
    try:
        data = resolve_req(req)
        priKey = data["priKey"]
        ip = data["ip"]
        print(data)
        handler = cr_handler(priKey, ip)
        ret = handler.getTransactionRes(data)
        return JsonResponse(ret)
    except Exception as err:
        print(err)
        return HttpResponse(err)
@csrf_exempt
def Course_Create(req):
    try:
        data = resolve_req(req)
        print(data)
        priKey = data["priKey"]
        ip = data["ip"]
        handler = cr_handler(priKey, ip)
        ret = dict()
        ret["txRet"] = handler.Course_Create(data)
        return JsonResponse(ret)
    except Exception as err:
        print(err)
        return HttpResponse(err)
