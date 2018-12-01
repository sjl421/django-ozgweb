from django.db import models
import json, time
from .commons import *

class Data(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 200)
	content = models.TextField()
	#data_class = models.ForeignKey(DataClass)	
	data_class_id = models.IntegerField(default = 0)
	sort = models.IntegerField(default = 0)
	type = models.IntegerField(default = 0)	
	hits = models.IntegerField(default = 0)
	picture = models.TextField()
	is_index_show = models.BooleanField(default = False)
	recommend = models.BooleanField(default = False)
	is_index_top = models.BooleanField(default = False)
	
	def toJSON(self):
		return to_json(self)
	
	class Meta:
		db_table = table_prefix + 'data'
	
	#获取分页数据，静态方法
	@staticmethod
	def getList(page, page_size, wq = { 'type': 0 }):
		total = Data.objects.filter(type = wq["type"]).count()
		page_count_s = commons.page_count(total, page_size)
	
		offset = (page - 1) * page_size
		limit = offset + page_size
	
		data_list = Data.objects.filter(type = wq["type"]).order_by("-sort", "-id")[offset:limit]
		data = []
		for i in data_list:
			item = json.loads(i.toJSON())
			item["add_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["add_time"]))
			data.append(item)
	
		data = {
			"page_size": page_size,
			"page_count": page_count_s,
			"total": total,
			"page": page,
			"list": data,
		}
		return data