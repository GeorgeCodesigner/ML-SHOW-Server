from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^linealReg/oneVar$', views.lr_oneVar, name='lr_oneVar'),
]