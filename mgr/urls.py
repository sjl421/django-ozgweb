
from django.urls import path
import mgr.views_index, mgr.views_other, mgr.views_user, mgr.views_art_single

app_name = 'mgr'

urlpatterns = [
	#后台页面部分
	path('index/login/', mgr.views_index.login),
	
	#验证码
	path('index/getvcode/', mgr.views_index.getvcode),
	
	#需要登录的
	path('other/server_info/', mgr.views_other.server_info),
	path('other/logout/', mgr.views_other.logout),
	path('user/updatepwd/', mgr.views_user.updatepwd),
	path('user/show/', mgr.views_user.show),
	path('user/add/', mgr.views_user.add),
	path('user/del/', mgr.views_user.userdel),
	path('art_single/get/', mgr.views_art_single.get),
	path('art_single/update/', mgr.views_art_single.update),
	
]
