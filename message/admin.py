from django.contrib import admin

# Register your models here.
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'created_time']
    fields = ['name', 'email', 'subject', 'message']


admin.site.register(Message, MessageAdmin)
