from django.shortcuts import render
import django
import os, json, hashlib, platform, time
import mgr.commons

def server_info(request):
	
	data = {
		"os": platform.system(),
		"django_version": django.get_version(),
		"python_version": platform.python_version(),
		"web_path": os.path.dirname(os.path.dirname(__file__)),
		"now": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
	}
	return mgr.commons.res_success("请求成功", data)
	
def logout(request):
	
	del request.session["user"]
	return mgr.commons.res_success("退出登录")
