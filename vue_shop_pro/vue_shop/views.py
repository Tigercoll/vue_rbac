from django.forms import model_to_dict
from django.db.models import Q
from django.shortcuts import render,HttpResponse
from django.http.response import JsonResponse,HttpResponseRedirect
from .models import Manager,Permission,Roles
from django.views.generic import View
from .forms import ManagerForm
from django.contrib.auth.hashers import make_password, check_password
# 导入JWT 包
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# 导入setting
from django.conf import settings
from django.http import QueryDict
import json
# 注册模块
class RegisterView(View):
    meta={}
    def post(self,request):
        username =request.POST.get('username','')
        password = request.POST.get('password','')
        password_2 =request.POST.get('password_2','')
        user = Manager.objects.filter(username=username)
        # 验证用户是否已存在
        if user:
            self.meta['msg'] = '用户已注册'
            self.meta['status'] = 400
            return JsonResponse({'meta': self.meta})
        # 验证两次密码是否一致
        if password!=password_2:
            self.meta['msg']='两次输入密码不一致!'
            self.meta['status']=400
            return JsonResponse({'meta':self.meta})
        manager_form = ManagerForm(request.POST)
        # 验证参数是否合法
        if not manager_form.is_valid():
            self.meta['msg']='请求参数有误!'
            self.meta['status']=400
            return JsonResponse({'meta':self.meta})
        post = manager_form.save(commit=False)
        # 给密码加密
        post.password = make_password(password,None,'pbkdf2_sha256')
        post.save()
        print(model_to_dict(post))
        data=model_to_dict(post)
        # 回传去掉密码
        data.pop('password')
        self.meta['msg']='注册成功'
        self.meta['status']=201
        print(data)
        return JsonResponse({'meta':self.meta,'data':data})

# 登录模块
class LoginView(View):
    meta = {}
    def post(self,request):
        username=request.POST.get('username','')
        password = request.POST.get('password','')

        user = Manager.objects.filter(username=username).first()

        if not user:
            self.meta['msg'] = '用户不存在'
            self.meta['status'] = 400
            return JsonResponse({'meta':self.meta})
        if not check_password(password,user.password):
            self.meta['msg'] = '密码不正确'
            self.meta['status'] = 400
            return JsonResponse({'meta': self.meta})
        self.meta['msg'] = '登录成功'
        self.meta['status'] = 200
        data = model_to_dict(user)
        token = self.generate_token(user.id,username)
        data.pop('password')
        data.update({'token':token})
        return JsonResponse({'meta':self.meta,'data':data})

    def generate_token(self,id,username):
        # 生成token
        serial = Serializer(secret_key=settings.SECRET_KEY,expires_in=3600)
        return serial.dumps({'id':id,'username':username}).decode('utf-8')

# 菜单栏模块
class MenusView(View):
    def get(self,request):
        # 如有需要可以在菜单栏获取的时候做权限控制
        # token =request.headers.get('Authorization')
        # serial = Serializer(secret_key=settings.SECRET_KEY)
        # userinfo = serial.loads(token)
        # print(userinfo)
        # user = Manager.objects.get(id=userinfo['id'],username=userinfo['username'])
        # per_list = user.role.permission.all()
        data={}

        per_list = Permission.objects.all()
        for per in per_list:
            if per.permission_level==0:
                data.update({per.id:{
                    "id": per.id,
                    "authName": per.permission_name,
                    "path": per.permission_url,
                    "children": []
                }})
        for per_2 in per_list:
            if per_2.permission_level==1:
                if per_2.permission_pid_id in data:
                    data[per_2.permission_pid_id]['children'].append({
                    "id": per_2.id,
                    "authName": per_2.permission_name,
                    "path": per_2.permission_url,
                    "children": []
                    })
        return JsonResponse({'meta':{
            'msg':'获取菜单成功',
            'status':200
        },
        'data':list(data.values())
        })

# 用户模块
class UserView(View):
    meta = {}
    '''
    {
    "data": {
        "totalpage": 5,
        "pagenum": 4,
        "users": [
            {
                "id": 25,
                "username": "tige117",
                "mobile": "18616358651",
                "type": 1,
                "email": "tige112@163.com",
                "create_time": "2017-11-09T20:36:26.000Z",
                "mg_state": true, // 当前用户的状态
                "role_name": "炒鸡管理员"
            }
        ]
    },
    "meta": {
        "msg": "获取成功",
        "status": 200
    }
}
    '''
    def get(self,request):
        query=request.GET.get('query','')
        pagenum=request.GET.get('pagenum','')
        pagesize=request.GET.get('pagesize','')
        # 验证参数
        try:
            pagenum =int(pagenum)
            pagesize=int(pagesize)
        except Exception as e:
            print(e)
            return JsonResponse({ "meta": {
        "msg": "参数错误",
        "status": 400
            }})
        if  query:
            print(query)
            users_list = Manager.objects.filter(username__contains=query)
        else:
            users_list = Manager.objects.all()[(pagenum - 1) * pagesize:pagenum * pagesize]
        total =  Manager.objects.count()
        users=[]
        for user in users_list:
            users.append({
                             "id": user.id,
                             "username": user.username,
                             "mobile": user.mobile,
                             "email": user.email,
                            "role_name": user.role and user.role.role_name or '未分配角色'
            })

        return JsonResponse({
            'data':{
                "totalpage": total,
                "pagenum":pagenum,
                "users": users
            },
            'meta':{
                'msg':'获取成功',
                "status": 200
            }
        })
    def post(self,request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = Manager.objects.filter(username=username)
        # 验证用户是否已存在
        if user:
            self.meta['msg'] = '用户已注册'
            self.meta['status'] = 400
            return JsonResponse({'meta': self.meta})
        manager_form = ManagerForm(request.POST)
        # 验证参数是否合法
        if not manager_form.is_valid():
            self.meta['msg'] = '请求参数有误!'
            self.meta['status'] = 400
            return JsonResponse({'meta': self.meta})
        post = manager_form.save(commit=False)
        # 给密码加密
        post.password = make_password(password, None, 'pbkdf2_sha256')
        post.save()
        print(model_to_dict(post))
        data = model_to_dict(post)
        # 回传去掉密码
        data.pop('password')
        self.meta['msg'] = '用户创建成功'
        self.meta['status'] = 201
        return JsonResponse({'meta': self.meta, 'data': data})

# 单用户查询修改删除
class UserDetailView(View):
    def get(self,request,id):
        userinfo =Manager.objects.filter(id=id).first()
        if not userinfo:
            return JsonResponse({
                "meta": {
                    "msg": "查询失败",
                    "status": 400
                }
            })
        return JsonResponse({
    "data": {
        "id": userinfo.id,
        "username": userinfo.username,
        "role_id": userinfo.role and userinfo.role.id or '',
        "mobile": userinfo.mobile,
        "email": userinfo.email
    },
    "meta": {
        "msg": "查询成功",
        "status": 200
    }
        })

    def put(self,request,id):
        data={}
        try:
            # Django对于PUT / DELETE请求并没有像POST / GET那样有一个字典结构。我们需要手动处理request.body获取参数：
            put = QueryDict(request.body)
            email = put.get('email','')
            mobile = put.get('mobile','')
            userinfo = Manager.objects.filter(id=id).first()
            userinfo.email=email
            userinfo.mobile=mobile
            userinfo.save()
            data={
                "id": userinfo.id,
                "username": userinfo.username,
                "role_id": userinfo.role and userinfo.role.role_name or '',
                "mobile": userinfo.mobile,
                "email": userinfo.email
            }
            meta={
                'msg': '更新成功', "status": 200
            }
        except Exception as e:
            print(e)
            meta={'msg':'更新失败', "status": 500}
        print({
    "data":data,
    "meta": meta
        })
        return JsonResponse({
    "data":data,
    "meta": meta
        })

    def delete(self,request,id):
        try:
            Manager.objects.filter(id=id).delete()
            meta ={
                "msg": "删除成功",
                "status": 200
            }
        except Exception as e:
            meta={
                "msg": "删除失败",
                "status": 500
            }
        return JsonResponse({'data':None,'meta':meta})

# 分配角色
class SetRoleView(View):
    def put(self,request,id):
        data={}
        meta={}
        try:
            put = QueryDict(request.body)
            rid= put.get('rid')
            user = Manager.objects.filter(id=id).first()
            user.role_id=rid
            user.save()
            data={
        "id": user.id,
        "rid": user.role_id,
        "username": user.username,
        "mobile": user.mobile,
        "email": user.email
    }
            meta={
                "msg": "设置角色成功",
                "status": 200
            }

        except Exception as e:
            print(e)
            meta = {
                "msg": "设置角色失败",
                "status": 400
            }
        print({
            'data':data,
            'meta':meta
        })
        return JsonResponse({
            'data':data,
            'meta':meta
        })

# 角色列表
class RolesListView(View):
    def get(self,request):
        data = []
        roles_obj =Roles.objects.all()
        for roles in roles_obj:
            role = {
                "id": roles.id,
                "roleName": roles.role_name,
                "roleDesc": roles.role_desc,
                "children":[]
            }
            roles_list={}
            for per in roles.permission.all():
              if per.permission_level==0:

                  roles_list[per.id]={
                      'id':per.id,
                      'authName':per.permission_name,
                      'path':per.permission_url,
                      'children':[]}
            # 二级菜单临时存放点
            temp ={}
            for per in roles.permission.all():
                if per.permission_level==1:
                    if per.permission_pid_id in roles_list:
                        temp[per.id] = {
                            'id': per.id,
                            'authName': per.permission_name,
                            'path': per.permission_url,
                            "pid": per.permission_pid_id,
                            'children': []
                        }
                        roles_list[per.permission_pid_id]['children'].append(
                            temp[per.id]
                        )

            for per in  roles.permission.all():
                if per.permission_level==2:
                    if per.permission_pid_id in temp:
                        temp[per.permission_pid_id]['children'].append(
                            {
                                "id": per.id,
                                "authName": per.permission_name,
                                "path": per.permission_url,
                                "pid": [temp[per.permission_pid_id]['pid'],per.permission_pid_id]
                            }
                        )
            role['children']=list((roles_list.values()))
            data.append(role)
        return JsonResponse({
            'data':data,
            'meta':{
                "msg": "获取成功",
                "status": 200
            }
        })
    # 添加权限
    def post(self,request):
        data={}
        try:
            roleName = request.POST.get('rolesName','')
            roleDesc = request.POST.get('rolesDesc','')
            Roles.objects.create(role_name=roleName,role_desc=roleDesc)
            roles_obj =Roles.objects.get(role_name=roleName,role_desc=roleDesc)
            data={
                "roleId": roles_obj.id,
                "roleName": roles_obj.role_name,
                "roleDesc": roles_obj.role_desc
            }
            meta={
                "msg": "创建成功",
                "status": 201
            }
        except Exception as e:
            print(e)
            meta = {
                "msg": "创建失败",
                "status": 500
            }
        return JsonResponse({
            'data':data,
            'meta':meta
        })

# 删除角色下的权限
class DelbyRoleIdRihthId(View):
    def delete(self,request,roleId,rightId):
        try:
            roles_obj = Roles.objects.get(id=roleId)
            per_obj= Permission.objects.filter(Q(id = rightId)|Q(permission_pid_id=rightId)|Q(permission_pid__permission_pid_id=rightId))
            roles_obj.permission.remove(*per_obj)
            data = self.get_per_list(roles_obj)
            return JsonResponse({
                'data':data,
                "meta": {
                    "msg": "取消权限成功",
                    "status": 200
                }
            })

        except Exception as e:
            print(e)
        return JsonResponse({
            "meta": {
                "msg": "取消权限失败",
                "status": 400
            }
        })


    def get_per_list(self,roles):
        roles_list = {}
        for per in roles.permission.all():
            if per.permission_level == 0:
                roles_list[per.id] = {
                    'id': per.id,
                    'authName': per.permission_name,
                    'path': per.permission_url,
                    'children': []}
        # 二级菜单临时存放点
        temp = {}
        for per in roles.permission.all():
            if per.permission_level == 1:
                if per.permission_pid_id in roles_list:
                    temp[per.id] = {
                        'id': per.id,
                        'authName': per.permission_name,
                        'path': per.permission_url,
                        "pid": per.permission_pid_id,
                        'children': []
                    }
                    roles_list[per.permission_pid_id]['children'].append(
                        temp[per.id]
                    )

        for per in roles.permission.all():
            if per.permission_level == 2:
                if per.permission_pid_id in temp:
                    temp[per.permission_pid_id]['children'].append(
                        {
                            "id": per.id,
                            "authName": per.permission_name,
                            "path": per.permission_url,
                            "pid": [temp[per.permission_pid_id]['pid'], per.permission_pid_id]
                        }
                    )
        return  list((roles_list.values()))

# 单角色的删改查
class RolesDetailView(View):
    # 通过id 获取角色信息
    def get(self,request,id):
        data={}
        meta={}
        try:
            roles_obj = Roles.objects.filter(id=id).first()
            data={
                "roleId": roles_obj.id,
                "roleName": roles_obj.role_name,
                "roleDesc": roles_obj.role_desc
            }
            meta={
                "msg": "获取成功",
                "status": 200
            }
        except Exception as e:
            meta={
                'msg':e,
                'status':500
            }
        return JsonResponse({'data':data,'meta':meta})

    #修改角色信息
    def put(self,request,id):
        data={}
        meta={}
        try:
            put = QueryDict(request.body)
            rolesName=put.get('rolesName')
            rolesDesc=put.get('rolesDesc')
            roles_obj=Roles.objects.get(id=id)
            roles_obj.role_name=rolesName
            roles_obj.role_desc=rolesDesc
            roles_obj.save()
            data = {
                "roleId": roles_obj.id,
                "roleName": roles_obj.role_name,
                "roleDesc": roles_obj.role_desc
            }
            meta={
                "msg": "获取成功",
                "status": 200
            }
        except Exception as e:
            meta={
                "msg": e,
                "status": 500
            }
        return JsonResponse({
            'data':data,'meta':meta
        })

    # 删除角色
    def delete(self,request,id):
        data = {}
        meta = {}
        try:
            Roles.objects.filter(id=id).delete()
            meta = {
                "msg": "删除成功",
                "status": 200
            }
        except Exception as e:
            meta = {
                'msg': e,
                'status': 500
            }
        return JsonResponse({'data': data, 'meta': meta})
    # 分配权限
    def post(self,reqeust,id):
        data={}
        meta={}
        try:

            rights_list = reqeust.POST.get('rights_list')
            rights_list=json.loads(rights_list)
            roles_obj = Roles.objects.get(id=id)
            roles_obj.permission.clear()
            per_obj_list = Permission.objects.filter(id__in=rights_list)
            roles_obj.permission.add(*per_obj_list)
            meta = {
                "msg": "更新成功",
                "status": 200
            }
        except Exception as e:
            meta = {
                "msg": "更新失败",
                "status": 500
            }
        return JsonResponse({
            'data':data,
            'meta':meta
        })

# 获取权限树
class RigthsView(View):
    def get(self,request,type):
        if type=='tree':
            data = {}
            try:
                per_obj = Permission.objects.all()
                data = self.get_per_list(per_obj)
                meta = {
                    "msg": "获取权限列表成功",
                    "status": 200
                }
            except Exception as e:

                meta = {
                    "msg": e,
                    "status": 500
                }
            return JsonResponse({
                'data':data,
                'meta':meta
            })
        elif type=='list':
            data = []
            try:
                per_obj = Permission.objects.all().order_by('permission_level')
                for per in per_obj:
                    data.append({
                "id": per.id,
                "authName": per.permission_name,
                "level": per.permission_level,
                "pid": per.permission_pid_id,
                "path": per.permission_url
            })

                meta={
                    "msg": "获取权限列表成功",
                    "status": 200
                }

            except  Exception as e:
                meta={
                    'msg':e,
                    'staust':500
                }
            return JsonResponse({
                'data': data,
                'meta':meta})
    def get_per_list(self,rigths_obj):
        roles_list = {}
        for per in rigths_obj:
            if per.permission_level == 0:
                roles_list[per.id] = {
                    'id': per.id,
                    'authName': per.permission_name,
                    'path': per.permission_url,
                    'level':per.permission_level,
                    'children': []}
        # 二级菜单临时存放点
        temp = {}
        for per in rigths_obj:
            if per.permission_level == 1:
                if per.permission_pid_id in roles_list:
                    temp[per.id] = {
                        'id': per.id,
                        'authName': per.permission_name,
                        'path': per.permission_url,
                        "pid": per.permission_pid_id,
                        'level': per.permission_level,
                        'children': []
                    }
                    roles_list[per.permission_pid_id]['children'].append(
                        temp[per.id]
                    )

        for per in rigths_obj:
            if per.permission_level == 2:
                if per.permission_pid_id in temp:
                    temp[per.permission_pid_id]['children'].append(
                        {
                            "id": per.id,
                            "authName": per.permission_name,
                            "path": per.permission_url,
                            'level': per.permission_level,
                            "pid": [temp[per.permission_pid_id]['pid'], per.permission_pid_id]
                        }
                    )
        return  list((roles_list.values()))

