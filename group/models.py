from django.db import models
from django.conf import settings
from django.urls import reverse



class Group(models.Model):
    name = models.CharField(max_length=25,unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True,default='')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,through='GroupMember')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(Group,related_name="memberships",on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="user_groups",on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group','user')
