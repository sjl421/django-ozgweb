from django.db import models
import json, time
from .commons import *

class DataClass(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 200)
	parent_id = models.IntegerField(default = 0)
	sort = models.IntegerField(default = 0)
	type = models.IntegerField(default = 0)
	
	def toJSON(self):
		return to_json(self)
	
	class Meta:
		db_table = table_prefix + 'data_class'
	
	#递归删除分类，静态方法
	@staticmethod
	def deleteById(id):
		dc_list = DataClass.objects.filter(parent_id = id)
	
		for dc in dc_list:
			child_count = DataClass.objects.filter(parent_id = dc.id).count()
			if child_count > 0:
				DataClass.deleteById(dc.id)
		
			#删除该分类下面的对应数据
			Data.objects.filter(dataclass_id = dc.id).delete()
			dc.delete()
			
	#递归获取父分类的dict，静态方法
	@staticmethod
	def getById(id):
		dataclass = DataClass.objects.get(id = id)
		dataclass_json = json.loads(dataclass.toJSON())	
		if dataclass_json["parent_id"] != 0:
			dataclass_json["parent"] = DataClass.getById(dataclass_json["parent_id"])	
		return dataclass_json
		
	#递归获取该分类下的分类(返回list)，静态方法
	@staticmethod
	def listById(id):
		dc_list = DataClass.objects.filter(parent_id = id).order_by("-sort", "-id")
		dc_list_json = []
		for dc in dc_list:
			item = json.loads(dc.toJSON())
				
			child_count = DataClass.objects.filter(parent_id = item["id"]).count()
			if child_count > 0:
				item["children"] = DataClass.listById(item["id"])
			
			dc_list_json.append(item)

		return dc_list_json
