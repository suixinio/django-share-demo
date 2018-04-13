import hashlib
import random
import string
import uuid

from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from share.models import Upload


class HomeView(View):
    def get(self, request):
        files = Upload.objects.all()
        for i in files:
            print(i)
        return render(request, "content.html", {'content': files})

    def post(self, request):
        if request.FILES:  # 如果有文件，向下执行，没有文件的情况,前端已经处理好。
            file = request.FILES.get("file")  # 获取文件
            name = file.name  # 获取文件名
            size = int(file.size)  # 获取文件大小
            uuid_code = HomeView.get_file_name()
            with open('static/file/' + uuid_code, 'wb')as f:  # 写文件到static/files
                f.write(file.read())

            # code = ''.join(random.sample(string.digits, 8))  # 生成随机八位的code
            print(request)
            u = Upload(
                path='static/file/' + uuid_code,
                name=name,
                file_size=size,
                code=uuid_code,
                PCIP=str(request.META['REMOTE_ADDR']),  # 获取上传文件的用户ip
            )
            u.save()  # 存储数据库
            return HttpResponsePermanentRedirect("/s/" + uuid_code)
            # 使用 HttpResponsePermanentRedirect 重定向到展示文件的页面.这里的 code 唯一标示一个文件。

    @classmethod
    def get_file_name(cls):
        uunum = uuid.uuid4()
        uustr = str(uunum)
        md5 = hashlib.md5()
        md5.update(uustr.encode('utf-8'))
        md5str = md5.hexdigest()
        return md5str


class DisplayView(View):
    def get(self, request, code):
        u = Upload.objects.filter(code=str(code))
        if u:
            for i in u:
                i.increase_views()
        return render(request, 'content.html', {'content': u})


class MyView(View):  # 定义一个MyView用于完成用户管理功能
    def get(self, request):
        IP = request.META['REMOTE_ADDR']  # 获取用户的IP
        u = Upload.objects.filter(PCIP=str(IP))  # 查找数据
        for i in u:
            i.increase_views()
        return render(request, 'content.html', {"content": u})  # 返回数据给前端
