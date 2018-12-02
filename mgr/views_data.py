from django.shortcuts import render
import django
import os, json, hashlib, platform, time
import mgr.commons, mgr.cfg

def show(request):
	#分页索引和每页显示数
	page = 1
	if request.GET.get("page"):
		page = int(request.GET.get("page"))
	page_size = mgr.cfg.page_size
	if request.GET.get("page_size"):
		page_size = int(request.GET.get("page_size"))
	
	wq = {
		"type": int(request.GET.get("type"))
	}
	
	res_data = Data.getList(page, page_size, wq)
	return commons.res_success("请求成功", res_data)

def get(request):		
	try:
		id = request.GET.get("id")
		id = int(id)
		data = Data.objects.get(id = id)
		
		return mgr.commons.res_success("请求成功", json.loads(data.toJSON()))
	except:
		return mgr.commons.res_fail(1, "找不到该数据")

def add(request):
	post_data = json.loads(request.body.decode("utf-8"))
	if "id" not in post_data:
		post_data["id"] = 0
	
	if post_data["name"]:
		return mgr.commons.res_fail(1, "名称不能为空")
	elif post_data["content"]:
		return mgr.commons.res_fail(1, "内容不能为空")
	
	data = None
	if id != 0:
		data = Data.objects.get(id = id)
	else:
		data = Data()
		data.hits = 0
		data.add_time = int(time.time())
	
	data.name = post_data["name"]
	data.content = post_data["content"]	
	data.data_class_id = post_data["data_class_id"]
	data.sort = post_data["sort"]
	data.type = post_data["type"]
	data.is_index_show = post_data["is_index_show"]
	data.is_index_top = post_data["is_index_top"]
	data.recommend = post_data["recommend"]
	data.picture = "[]"
	data.save()
	
	if id != 0:
		return mgr.commons.res_success("更新成功")
	else:
		return mgr.commons.res_success("添加成功")

def datadel(request):

	ids = request.GET.get("ids")
	ids = ids.split(",")
	
	if len(ids) == 0:
		return mgr.commons.res_fail(1, "没有需要删除的数据")
	
	try:
		for id in ids:
			id = int(id)
			
			try:
				data = Data.objects.get(id = id)
				data.delete()
			except:
				return mgr.commons.res_fail(1, "删除数据id为" + str(id) + "时出现错误")
		
		return mgr.commons.res_success("删除成功")
	except:
		return mgr.commons.res_fail(1, "删除数据时出现错误")
