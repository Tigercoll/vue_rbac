from django.db import models

# Create your models here.

class Manager(models.Model):
    username = models.CharField(max_length=64,verbose_name='用户名')
    password = models.CharField(max_length=128,verbose_name='密码')
    mobile = models.CharField(max_length=32,verbose_name='电话',blank=True,null=True)
    email = models.EmailField(max_length=64,verbose_name='邮箱',blank=True,null=True)
    role = models.ForeignKey(to='Roles',verbose_name='角色',null=True,blank=True,on_delete=models.CASCADE)

class Roles(models.Model):
    role_name = models.CharField(max_length=32,verbose_name='角色名',null=True,blank=True)
    role_desc = models.CharField(max_length=64,verbose_name='角色描述',null=True,blank=True)
    permission = models.ManyToManyField(to='Permission',verbose_name='权限',blank=True)

class Permission(models.Model):
    permission_name = models.CharField(max_length=32,verbose_name='权限名',null=True,blank=True)
    permission_url = models.CharField(max_length=64,verbose_name='权限url',null=True,blank=True)
    permission_pid = models.ForeignKey(to='self',null=True,blank=True,verbose_name='权限父ID',on_delete=models.CASCADE)
    permission_level = models.IntegerField(verbose_name='权限等级',null=True,blank=True)

