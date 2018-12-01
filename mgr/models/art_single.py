from django.db import models
import json, time
from .commons import *

class ArtSingle(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 200)
	content = models.TextField()
	
	def toJSON(self):
		return to_json(self)
	
	class Meta:
		db_table = table_prefix + 'art_single'
