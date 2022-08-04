
from django.contrib import admin
from django.urls import path
from .views import helloworldfunc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', helloworldfunc),
]
