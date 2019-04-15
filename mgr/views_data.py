from django.shortcuts import render
import django
import os, json, hashlib, platform, time
import mgr.commons, mgr.cfg
from .models import *

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
	
	if request.GET.get("k_name"):
		wq["name__contains"] = request.GET.get("k_name")
	
	if request.GET.get("k_data_cat_id"):
		wq["data_cat_id"] = int(request.GET.get("k_data_cat_id"))
	
	res_data = Data.getList(page, page_size, wq)
	return mgr.commons.res_success("请求成功", res_data)

def get(request):		
	try:
		id = request.GET.get("id")
		id = int(id)
		data = Data.objects.get(id = id)
		data = json.loads(data.toJSON())
		data["picture"] = json.loads(data["picture"])
		return mgr.commons.res_success("请求成功", data)
	except:
		return mgr.commons.res_fail(1, "找不到该数据")

def add(request):
	post_data = json.loads(request.body.decode("utf-8"))
	if "id" not in post_data:
		post_data["id"] = 0
	
	if post_data["name"] == "":
		return mgr.commons.res_fail(1, "名称不能为空")
	elif post_data["content"] == "":
		return mgr.commons.res_fail(1, "内容不能为空")
	
	data = None
	if post_data["id"] != 0:
		data = Data.objects.get(id = post_data["id"])
		
		if "picture" in post_data:
			data.picture = json.dumps(post_data["picture"])
	else:
		data = Data()
		data.hits = 0
		data.add_time = int(time.time())
		if "picture" in post_data:
			data.picture = json.dumps(post_data["picture"])
		else:
			data.picture = "[]"
	
	data.name = post_data["name"]
	data.content = post_data["content"]	
	data.data_cat_id = post_data["data_cat_id"] if "data_cat_id" in post_data else 0
	data.sort = post_data["sort"]
	data.type = post_data["type"]
	data.is_index_show = post_data["is_index_show"] if "is_index_show" in post_data else 0
	data.is_index_top = post_data["is_index_top"] if "is_index_top" in post_data else 0
	data.recommend = post_data["recommend"] if "recommend" in post_data else 0
	data.save()
	
	if post_data["id"] != 0:
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

def handle_uploaded_file(f):
	file_name = None
	
	ext_name = os.path.splitext(f.name)[1]
	
	max_size = mgr.cfg.max_upload
	
	#允许上传的文件类型
	allow_ext_name = [
		".jpg",
		".jpeg",
		".png",
		".gif",
	];	
	
	if ext_name not in allow_ext_name:
		return {
			"msg": "不允许上传此类文件",
			"filepath": file_name
		}
	
	if f.size > max_size:
		return {
			"msg": "不能上传超过" + str(max_size // 1024 // 1024) + "M的文件",
			"filepath": file_name
		}
	
	try:
		base_path = os.path.dirname(os.path.dirname(__file__))
		path = base_path + "/static/upload/" + time.strftime('%Y/%m/%d/')
		if not os.path.exists(path):
			os.makedirs(path)
		
		file_exists = True
		while file_exists:
			m = hashlib.md5()
			m.update(str(time.time()).encode(encoding = 'UTF-8'))
			
			file_name = path + m.hexdigest() + ext_name
			file_exists = os.path.exists(file_name)
			if file_exists:
				time.sleep(1)
		
		destination = open(file_name, 'wb+')
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close()
		
		file_name = file_name.replace(base_path + "/static/upload/", "")
		
	except Exception as e:
		return {
			"msg": str(e),
			"filepath": file_name
		}

	return {
		"msg": "上传成功",
		"filepath": file_name
	}

def upload(request):
	f = request.FILES['file']
	res_f = handle_uploaded_file(f)
	if res_f["filepath"] != None:		
		return mgr.commons.res_success(res_f["msg"], { "filepath": res_f["filepath"] })
	else:
		return mgr.commons.res_fail(1, res_f["msg"])
