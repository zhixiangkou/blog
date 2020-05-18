from django.db import models

# Create your models here.
from django.utils import timezone


class Message(models.Model):
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    subject = models.CharField('主题', max_length=50)
    message = models.TextField('消息')
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.name
