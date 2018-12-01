
#model的公用部分
from django.db import models
from django.http import JsonResponse
import json

table_prefix = 't_'

def to_json(obj):
	fields = []
	for field in obj._meta.fields:
		fields.append(field.name)
	d = {}
	for attr in fields:
		val = getattr(obj, attr)
		
		#如果是model类型，就要再一次执行model转json
		if isinstance(val, models.Model):
			val = json.loads(to_json(val))
		d[attr] = val
	return json.dumps(d)

#计算总页数
def page_count(count, page_size):
	if count % page_size == 0:
		return (count // page_size)
	else:
		return (count // page_size) + 1
