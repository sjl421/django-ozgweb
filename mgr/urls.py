
from django.urls import path
import mgr.views_index, mgr.views_other, mgr.views_user, mgr.views_art_single, mgr.views_data, mgr.views_data_cat

app_name = 'mgr'

urlpatterns = [
	#登录页面
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
	path('data/show/', mgr.views_data.show),
	path('data/get/', mgr.views_data.get),
	path('data/add/', mgr.views_data.add),
	path('data/del/', mgr.views_data.datadel),
	path('data/upload/', mgr.views_data.upload),
	path('data_cat/show/', mgr.views_data_cat.show),
	path('data_cat/get/', mgr.views_data_cat.get),
	path('data_cat/add/', mgr.views_data_cat.add),
	path('data_cat/del/', mgr.views_data_cat.data_cat_del),
]
