from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import os
import uuid
from PIL import Image


def testApi(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        User.objects.create(username=username)
        return HttpResponse(1)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            User.objects.get(username=username)
            return HttpResponse(1)
        except:
            User.objects.create(username=username, password=password, passed=2, role=0)
            return HttpResponse(1)
        
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if user.username == username and user.password == password:
                resp = {
                    "username": user.username,
                    "role": user.role,
                }
                return JsonResponse(resp)
            else:
                return HttpResponse(0)
        except:
            return HttpResponse(0)



def validateUserExist(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        try:
            User.objects.get(username=username)
            return HttpResponse(1)
        except:
            return HttpResponse(0)


@csrf_exempt
def receive(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_name = str(uuid.uuid4()) + '_' + file.name
        file_path = os.path.join('.\\data', file_name)

        id = request.POST.get('id')
        username = request.POST.get('username')
        name = request.POST.get('name')
        school = request.POST.get('school')
        passed = request.POST.get('passed')
        qq = request.POST.get('qq')

        print(id, username, name, school, passed, qq)

        with open(file_path, 'wb') as wf:
            wf.write(file.read())


        # 打开图片并进行压缩
        image = Image.open(file_path)
        compressed_image = image.copy()  # 创建副本用于压缩
        compressed_image.thumbnail((1024, 1024))  # 设置压缩后的尺寸，这里设置为最长边不超过800像素
        compressed_image.save(file_path)


        user = User.objects.get(username=username)
        user.name = name
        user.school = school
        user.qq = qq
        user.image_url = file_path

        user.save()

        return HttpResponse('success')
    

def getUserInfo(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        try:
            user = User.objects.get(username=username)
            
            resp = {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'school': user.school,
                'qq': user.qq,
                'passed': user.passed,
                'updated_at': user.updated_at,
                'role': user.role,
            }

            return JsonResponse(resp)
        except:
            return HttpResponse(0)

def getQRCode(request):
    if request.method == 'GET':
        with open('.\\global\\qrcode.jpg', 'rb') as rf:
            image_data = rf.read()
            return HttpResponse(image_data, content_type='image/jpeg')
        

def setUserPassed(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        passed = request.GET.get('passed')
        user = User.objects.get(username=username)
        user.passed = passed
        user.save()
        return HttpResponse(1)
    

def sort_by_updated_at(users):
    users.sort(key=lambda user: user['updated_at'], reverse=True)
    return users
    

def getAll(request):
    if request.method == 'GET':
        users = User.objects.all()
        all_users = []
        for user in users:
            if (user.name and user.school and user.qq):
                all_users.append({
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'school': user.school,
                    'qq': user.qq,
                    'passed': user.passed,
                    'updated_at': user.updated_at
                })

        return JsonResponse(sort_by_updated_at(all_users),  safe=False)
    

def getAllNotPass(request):
    if request.method == 'GET':
        users = User.objects.all()
        all_users = []
        for user in users:
            if (user.name and user.school and user.qq and user.passed == 0):
                all_users.append({
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'school': user.school,
                    'qq': user.qq,
                    'passed': user.passed,
                    'updated_at': user.updated_at
                })

        return JsonResponse(sort_by_updated_at(all_users),  safe=False)
    
def getUserImage(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.get(username=username)
        image_url = user.image_url
        with open(image_url, 'rb') as rf:
            image_data = rf.read()
            return HttpResponse(image_data, content_type='image/jpeg')
        