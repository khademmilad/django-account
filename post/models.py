from django.db import models
from django.conf import settings


from group.models import Group


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="posts",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    group = models.ForeignKey(Group,related_name='post',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.username,'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','message']
