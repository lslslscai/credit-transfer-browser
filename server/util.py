from pymongo import MongoClient
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

def get_db_handle(db_name, host):
    client = MongoClient(host)
    db_handle = client[db_name]
    return db_handle, client

@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)  # 获取csrf_token的值
    print(request, csrf_token)
    return JsonResponse({'token': csrf_token})

