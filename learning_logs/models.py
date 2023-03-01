from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model) :
    # the topic user is learning About
    text = models.CharField(max_length=25)
    date_added = models.DateTimeField(auto_now_add = True)
    owner =models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self) :
        """stringe representation of the class:"""
        return self.text
    
class Entry(models.Model):
    # the entry of each topic selected
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)
    class Meta :
        verbose_name_plural = 'entries'
    
    def __str__(self):
        return self.text
    
    
