from django.db import models

class user(models.Model):
	uid=models.BigIntegerField(primary_key=True)
	access_token=models.CharField(max_length=100)
	name=models.CharField(max_length=50)
	photo=models.URLField()
class shit(models.Model):
	user=models.ForeignKey(user)
	text=models.CharField(max_length=200)
	time=models.DateTimeField(auto_now=True)






