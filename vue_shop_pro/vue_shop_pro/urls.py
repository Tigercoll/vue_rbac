"""vue_shop_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vue_shop.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/private/v1/register', RegisterView.as_view()),
    path('api/private/v1/login', LoginView.as_view()),
    # 左侧菜单栏
    path('api/private/v1/menus', MenusView.as_view()),
    path('api/private/v1/users', UserView.as_view()),
    path('api/private/v1/rights/<str:type>', RigthsView.as_view()),
    path('api/private/v1/users/<int:id>/role', SetRoleView.as_view()),
    path('api/private/v1/roles', RolesListView.as_view()),
    path('api/private/v1/roles/<int:id>', RolesDetailView.as_view()),
    path('api/private/v1/users/<int:id>', UserDetailView.as_view()),
    path('api/private/v1/roles/<int:roleId>/rights/<int:rightId>', DelbyRoleIdRihthId.as_view()),
]
