from django.db import models

# Create your models here.

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    number = models.IntegerField()#default=0)
    
    class Meta:
        db_table = 'table1'