"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from Backend import api_urls 

from django.conf import settings
def create_role(name):

    try:
        from django.contrib.auth.models import Group, Permission
        group = Group.objects.create(name=name)
        group.save()
    except Exception as e:
        print(e)

create_role("query_admin")
create_role("central_admin")
create_role("branch_admin")
create_role("branch_user")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls'))

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
