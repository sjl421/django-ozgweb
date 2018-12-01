from django.shortcuts import render
import django
import os, json, hashlib, platform, time
import mgr.commons
from .models import *

def index_login(request):
	if request.method != 'POST':
		return mgr.commons.res_fail(1, "请使用POST方式提交")
	
	post_data = json.loads(request.body.decode("utf-8"))
	if "vcode" not in post_data:
		post_data["vcode"] = None
	print(post_data["name"] + "========")
	user = None
	try:
		user = User.objects.get(name = post_data["name"])
	except Exception as e:
		return mgr.commons.res_fail(1, "没有此用户")
	
	if user.err_login >= 3:
		if post_data["vcode"] == None:
			return mgr.commons.res_fail(2, "输入错误密码次数过多，需要输入验证码")
		elif post_data["vcode"] == "":
			return mgr.commons.res_fail(2, "验证码不能为空")
		else:
			ca = mgr.commons.Captcha(request)
			if ca.check(post_data["vcode"]) == False:
				return mgr.commons.res_fail(3, "验证码错误")
			
	m = hashlib.md5()
	m.update(post_data["pwd"].encode(encoding = 'UTF-8'))			
	pwd_md5 = m.hexdigest()
			
	if user.pwd == pwd_md5:
		user.err_login = 0
		user.save()
				
		user_jsonstr = user.toJSON()
		user = json.loads(user_jsonstr)
		del(user["pwd"])
		request.session["user"] = user
				
		return mgr.commons.res_success("登录成功", user)
	else:
		user.err_login += 1
		user.save()
		return mgr.commons.res_fail(1, "密码错误")

def index_getvcode(request):
	ca = mgr.commons.Captcha(request)
	#ca.words = ['hello', 'world', 'helloworld']
	ca.type = 'number' #or word
	ca.img_width = 150
	ca.img_height = 30
	return ca.display()

def other_server_info(request):
	
	data = {
		"os": platform.system(),
		"django_version": django.get_version(),
		"python_version": platform.python_version(),
		"web_path": os.path.dirname(os.path.dirname(__file__)),
		"now": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
	}
	return mgr.commons.res_success("请求成功", data)
	
	