from django.db import models

class Place(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=150,default='음식점')
    link = models.CharField(max_length=150,blank=True)
    image = models.URLField(null=True)
    description = models.TextField(default='증말 맛있어요!')
    user = models.ForeignKey('users.User',on_delete=models.CASCADE)
    like_user = models.ManyToManyField('users.User',related_name='like_user',blank=True)
    hate_user = models.ManyToManyField('users.User',related_name='hate_user',blank=True)

    def count_likes(self):
        return self.like_user.count()
    
    def count_hates(self):
        return self.hate_user.count()