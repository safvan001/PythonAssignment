from django.contrib import admin
from django.urls import path
from citations.views import *

urlpatterns = [
    path('',index,name='home')
]
