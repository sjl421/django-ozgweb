from django.shortcuts import render
import django
import os, json, hashlib, platform, time
import mgr.commons, mgr.cfg
from .models import *

def updatepwd(request):
	
	curr_user = request.session.get("user")
	post_data = json.loads(request.body.decode("utf-8"))
	
	if post_data["old_pwd"] == "":
		return mgr.commons.res_fail(1, "旧密码不能为空")
	if post_data["pwd"] == "":
		return mgr.commons.res_fail(1, "新密码不能为空")
	if post_data["pwd"] != post_data["pwd2"]:
		return mgr.commons.res_fail(1, "确认密码不正确")
	
	m = hashlib.md5()
	m.update(post_data["old_pwd"].encode(encoding = 'UTF-8'))			
	post_data["old_pwd"] = m.hexdigest()
	
	try:
		user = User.objects.get(name = curr_user["name"], pwd = post_data["old_pwd"])
		
		m = hashlib.md5()
		m.update(post_data["pwd"].encode(encoding = 'UTF-8'))			
		post_data["pwd"] = m.hexdigest()
		
		user.pwd = post_data["pwd"]
		user.save()
	
		return mgr.commons.res_success("修改密码成功")
	except:
		return mgr.commons.res_fail(1, "旧密码不正确")

def show(request):
	#分页索引和每页显示数
	page = 1
	if request.GET.get("page"):
		page = int(request.GET.get("page"))
	page_size = mgr.cfg.page_size
	if request.GET.get("page_size"):
		page_size = int(request.GET.get("page_size"))
	
	res_data = User.getList(page, page_size)
	
	return mgr.commons.res_success("请求成功", res_data)
	
def add(request):
	post_data = json.loads(request.body.decode("utf-8"))
	
	if post_data["name"] == "":
		return mgr.commons.res_fail(1, "用户名不能为空")
	if post_data["pwd"] == "":
		return mgr.commons.res_fail(1, "密码不能为空")
	
	total = User.objects.filter(name = post_data["name"]).count()
	if total > 0:
		return mgr.commons.res_fail(1, "该用户已存在")
	
	user = User(
		name = post_data["name"],
		pwd = post_data["pwd"],
		add_time = int(time.time())
	)
	user.save()
	
	return mgr.commons.res_success("添加成功", json.loads(user.toJSON()))
	
def userdel(request):
	
	ids = request.GET.get("ids")
	ids = ids.split(",")
	
	if len(ids) == 0:
		return mgr.commons.res_fail(1, "没有需要删除的数据")
	
	try:
		curr_user = request.session.get("user")
		for id in ids:
			id = int(id)
			if curr_user["id"] == id:
				return mgr.commons.res_fail(1, "不能删除自己")
			
			try:
				user = User.objects.get(id = id)
				user.delete()
			except:
				return mgr.commons.res_fail(1, "删除数据id为" + str(id) + "时出现错误")
		
		return mgr.commons.res_success("删除成功")
	except:
		return mgr.commons.res_fail(1, "删除数据时出现错误")

