from django.db import models

class Place(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    image = models.URLField(null=True)
    description = models.TextField(default='증말 맛있어요!')
    likes_num = models.PositiveIntegerField(default=0)
    hates_num = models.PositiveIntegerField(default=0) 
    user = models.ForeignKey('users.User',on_delete=models.CASCADE)
    like_user = models.ManyToManyField('users.User',related_name='like_user',blank=True)
    hate_user = models.ManyToManyField('users.User',related_name='hate_user',blank=True)