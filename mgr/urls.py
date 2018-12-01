
from django.urls import path
import mgr.views

app_name = 'mgr'

urlpatterns = [
	#后台页面部分
	path('index/login/', mgr.views.index_login),
	
	#验证码
	path('index/getvcode/', mgr.views.index_getvcode),
	
	#需要登录的
	path('other/server_info/', mgr.views.other_server_info),
	
	
]
