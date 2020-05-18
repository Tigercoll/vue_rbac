import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import  HttpResponse,redirect
from ..models import Manager
from itsdangerous import TimedJSONWebSignatureSerializer as  Serial
from django.http import JsonResponse
from django.conf import settings
class TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 获取url后缀
        url_path = request.path_info

        # 是否登录
        if  url_path=='/api/private/v1/login' or url_path=='/api/private/v1/register' or '/admin':
            return None
        try:
            token=request.META.get('HTTP_AUTHORIZATION','')
            if not token:
                raise Exception('没有token')
            serial = Serial(secret_key=settings.SECRET_KEY)
            userinfo = serial.loads(token)

            user = Manager.objects.filter(username=userinfo['username'],id=userinfo['id'])
            if not user:
                raise Exception('token错误')
            request.user=userinfo
        except:
            return JsonResponse({'meta': {'msg': '认证失败', 'status': 401}})
        return None
        # if not token:
        #     return redirect("/api/private/v1/login")

        # 检验权限
        # for permission in permission_dict.values():
        #     urls = permission['urls']
        #     for url in urls:
        #         url = '^%s$' % url
        #         ret = re.match(url, url_path)
        #         if ret:
        #             # 将动作加入request用于判断用户有没有这个操作权限
        #             request.actions = permission['actions']
        #             return None
        # return HttpResponse('没有权限')