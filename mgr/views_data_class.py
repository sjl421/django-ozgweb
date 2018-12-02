from django.shortcuts import render
import django
import os, json, hashlib, platform, time
import mgr.commons, mgr.cfg
from .models import *

def show(request):
	
	type = int(request.GET.get("type"))
	data_class_list = DataClass.objects.filter(type = type, parent_id = 0).order_by("-sort", "-id")
	data_class_list_json = []
	for data_class in data_class_list:		
		item = json.loads(data_class.toJSON())
		
		child_count = DataClass.objects.filter(parent_id = item["id"]).count()
		if child_count > 0:
			item["children"] = DataClass.listById(item["id"])
			
		data_class_list_json.append(item)
	
	return mgr.commons.res_success("请求成功", data_class_list_json)

def get(request):
		
	try:
		id = request.GET.get("id")
		data_class = DataClass.objects.get(id = id)
		
		#该分类下的数据
		#test = dataclass.data_set.all()
		#print(test.count())
		
		data_class_json = json.loads(data_class.toJSON())
		if data_class_json["parent_id"] != 0:
			data_class_json["parent"] = DataClass.getById(data_class_json["parent_id"])
		
		return mgr.commons.res_success("请求成功", data_class_json)
	except:
		return mgr.commons.res_fail(1, "找不到该数据")

def add(request):
	post_data = json.loads(request.body.decode("utf-8"))
	
	if "id" not in post_data:
		post_data["id"] = 0
			
	data_class = None
	if post_data["id"] != 0:
		if post_data["id"] == post_data["parent_id"]:
			return mgr.commons.res_fail(1, "父级分类不能为当前选中分类")
		
		data_class = DataClass.objects.get(id = post_data["id"])
	else:
		data_class = DataClass()
	
	data_class.name = post_data["name"]
	data_class.parent_id = post_data["parent_id"]
	data_class.sort = post_data["sort"]
	data_class.type = post_data["type"]
	data_class.save()
	
	if post_data["id"] != 0:
		return mgr.commons.res_success("更新成功")
	else:
		return mgr.commons.res_success("添加成功")

def data_class_del(request):
	
	id = int(request.GET.get("id"))
	try:
		data_class = DataClass.objects.get(id = id)
		
		child_count = DataClass.objects.filter(parent_id = data_class.id).count()
		if child_count > 0:
			DataClass.deleteById(data_class.id)
		
		#删除该分类下面的对应数据
		Data.objects.filter(data_class_id = data_class.id).delete()
		data_class.delete()
		
		return mgr.commons.res_success("删除成功")
	except:
		return mgr.commons.res_fail(1, "该数据不存在")
