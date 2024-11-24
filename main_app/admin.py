from django.contrib import admin
from .models import User, TelegramBotConfig, Task, AliExpressApi, AmazonApi

admin.site.register(User)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'start_time')


@admin.register(TelegramBotConfig)
class TelegramBotConfigAdmin(admin.ModelAdmin):
    list_display = ('bot_name', 'channel_name', 'is_enabled')


@admin.register(AliExpressApi)
class AliExpressApiAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if AliExpressApi.objects.all().count() >= 1:
            return False
        return True


@admin.register(AmazonApi)
class AmazonApiAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if AmazonApi.objects.all().count() >= 1:
            return False
        return True
