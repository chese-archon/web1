from django.db import models
from django.db.models.signals import pre_save, post_save  #Inbuilt Signals
from django.dispatch import receiver
# Create your models here.

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    number = models.IntegerField()#default=0)
    
    class Meta:
        db_table = 'table1'

# test signals
last_signal_message = None

@receiver(pre_save, sender=Data)
def save_pre(sender, instance, **kwargs):
    global last_signal_message
    last_signal_message = "Pre save model data signal"
    print(last_signal_message)  # Выводим в консоль

@receiver(post_save, sender=Data)
def save_post(sender, instance, **kwargs):
    global last_signal_message
    last_signal_message = "Post save model data signal"
    print(last_signal_message)  # Выводим в консоль
    

"""
def save_pre(sender, instance, **kwargs):
    global last_signal_message
    last_signal_message = "Pre save model data signal"
    print(last_signal_message)

def save_post(sender, instance, **kwargs):
    #global last_signal_message
    last_signal_message = "Post save model data signal"
    print(last_signal_message)

pre_save.connect(save_pre, sender=Data) # This will trigger after the saving data into Post model
post_save.connect(save_post, sender=Data)"
"""
