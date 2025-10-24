"""
URL configuration for user project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework.authtoken.views import obtain_auth_token
from blogs import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/token/', obtain_auth_token),

    
    path('api/v1/posts/', views.post_list_create),
    path('api/v1/posts/<int:pk>/', views.post_detail),

    path('api/v1/posts/<int:post_id>/comments/', views.comment_list_create),
]
