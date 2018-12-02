from django.shortcuts import render
import django
import os, json, hashlib, platform, time
import mgr.commons, mgr.cfg
from .models import *

def get(request):
	
	id = request.GET.get("id")
	id = int(id)
	
	obj = ArtSingle.objects.get(id = id)
	return mgr.commons.res_success("请求成功", json.loads(obj.toJSON()))

def update(request):
	post_data = json.loads(request.body.decode("utf-8"))
	post_data["id"] = int(post_data["id"])
	
	obj = ArtSingle.objects.get(id = post_data["id"])
	obj.content = post_data["content"]
	
	obj.save()
	return mgr.commons.res_success("更新成功")
