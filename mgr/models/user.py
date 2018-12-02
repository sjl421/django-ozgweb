from django.db import models
import json, time
from .commons import *

class User(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 200)
	pwd = models.CharField(max_length = 200)
	add_time = models.IntegerField(default = 0)
	is_admin = models.BooleanField(default = False)
	err_login = models.IntegerField(default = 0)
	
	def toJSON(self):
		return to_json(self)
	
	class Meta:
		db_table = table_prefix + 'user'
	
	#获取分页数据，静态方法
	@staticmethod
	def getList(page, page_size):
		total = User.objects.all().count()
		page_count_s = page_count(total, page_size)
	
		offset = (page - 1) * page_size
		limit = offset + page_size
		data_list = User.objects.all().order_by("-id")[offset:limit]
	
		data_list_json = []
		for data in data_list:		
			item = json.loads(data.toJSON())
			item["add_time_s"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["add_time"]))
			
			#移除密码
			del item["pwd"]
			data_list_json.append(item)
	
		data = {
			"page_size": page_size,
			"page_count": page_count_s,
			"total": total,
			"page": page,
			"list": data_list_json,
		}
		return data		
