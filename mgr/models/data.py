from django.db import models
import json, time
from .commons import *
from .data_class import DataClass

class Data(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 200)
	content = models.TextField()
	
	#on_delete是必须参数，对应的外键就不需要了，外键的命名规则是关联类的小写加上_id，默认情况下关联到关联类的主键，to_field可修改关联类的字段
	data_class = models.ForeignKey(DataClass, null = True, on_delete = models.CASCADE)	
	#data_class_id = models.IntegerField(default = 0)
	sort = models.IntegerField(default = 0)
	type = models.IntegerField(default = 0)	
	hits = models.IntegerField(default = 0)
	picture = models.TextField()
	add_time = models.IntegerField(default = 0)
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
		total = Data.objects.filter(**wq).count()
		page_count_s = page_count(total, page_size)
	
		offset = (page - 1) * page_size
		limit = offset + page_size
	
		data_list = Data.objects.filter(**wq).order_by("-sort", "-id")[offset:limit]
		
		data = []
		for i in data_list:
			item = json.loads(i.toJSON())
			item["add_time_s"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["add_time"]))
			item["picture"] = json.loads(item["picture"])
			
			if item["data_class"]["id"] == 0:
				item["dc_name"] = "[无分类]"
			else:
				item["dc_name"] = i.data_class.name
			data.append(item)
	
		data = {
			"page_size": page_size,
			"page_count": page_count_s,
			"total": total,
			"page": page,
			"list": data,
		}
		return data