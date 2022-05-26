from django.contrib import admin
from .models import MyThread, ChatMessage

# Register your models here.


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessageInline]

    class Meta:
        model = MyThread


admin.site.register(MyThread, ThreadAdmin)
# Register your models here.
