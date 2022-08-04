
from django.contrib import admin
from django.urls import path,include
from .views import helloworldfunc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', helloworldfunc),
    path('', include("search.urls"),name="search"),
]
