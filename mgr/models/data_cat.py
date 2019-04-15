from django.db import models
from django.db import connection
import json, time
from .commons import *

class DataCat(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 200)
	parent_id = models.IntegerField(default = 0)
	sort = models.IntegerField(default = 0)
	type = models.IntegerField(default = 0)
	
	def toJSON(self):
		return to_json(self)
	
	class Meta:
		db_table = table_prefix + 'data_cat'
	
	#递归删除分类，静态方法
	@staticmethod
	def deleteById(id):
		dc_list = DataCat.objects.filter(parent_id = id)
	
		for dc in dc_list:
			child_count = DataCat.objects.filter(parent_id = dc.id).count()
			if child_count > 0:
				DataCat.deleteById(dc.id)
		
			#删除该分类下面的对应数据
			cursor = connection.cursor()
			cursor.execute("delete from " + table_prefix + "data where data_cat_id = " + str(dc.id))
			cursor.close()
			
			dc.delete()
			
	#递归获取父分类的dict，静态方法
	@staticmethod
	def getById(id):
		data_cat = DataCat.objects.get(id = id)
		data_cat_json = json.loads(data_cat.toJSON())	
		if data_cat_json["parent_id"] != 0:
			data_cat_json["parent"] = DataCat.getById(data_cat_json["parent_id"])	
		return data_cat_json
		
	#递归获取该分类下的分类(返回list)，静态方法
	@staticmethod
	def listById(id):
		dc_list = DataCat.objects.filter(parent_id = id).order_by("-sort", "-id")
		dc_list_json = []
		for dc in dc_list:
			item = json.loads(dc.toJSON())
				
			child_count = DataCat.objects.filter(parent_id = item["id"]).count()
			if child_count > 0:
				item["children"] = DataCat.listById(item["id"])
			
			dc_list_json.append(item)

		return dc_list_json
