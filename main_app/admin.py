from django.contrib import admin
from django import forms
from .models import User, TelegramBotConfig, AliExpressApi, AmazonApi, AmazonManualTask, AmazonAutomationTask

admin.site.register(User)


class AmazonManualTaskModelForm(forms.ModelForm):
    class Meta:
        model = AmazonManualTask
        fields = '__all__'

    bot = forms.ModelMultipleChoiceField(
        queryset=TelegramBotConfig.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def clean_asins(self):
        asins = self.cleaned_data['asins']

        if not type(asins) is list:
            self.add_error(
                "asins",
                "The field must be empty, for example: [] or contain a list "
                'of ASIN\'s in the following JSON format: ["ASIN", "ASIN"].',
            )

        return asins


# @admin.register(AmazonManualTask)
# class AmazonManualTaskAdmin(admin.ModelAdmin):
#     form = AmazonManualTaskModelForm
#     list_display = ('name', 'status', 'start_time')

class AmazonAutoTaskModelForm(forms.ModelForm):
    class Meta:
        model = AmazonAutomationTask
        fields = '__all__'

    def clean_num_items(self):
        value = self.cleaned_data['num_items']
        if value < 1 or value > 10:
            raise forms.ValidationError('Value must be between 1 and 10.')
        return value

@admin.register(AmazonAutomationTask)
class AmazonAutoTaskAdmin(admin.ModelAdmin):
    form = AmazonAutoTaskModelForm
    list_display = ('name', 'status', 'start_time')


@admin.register(TelegramBotConfig)
class TelegramBotConfigAdmin(admin.ModelAdmin):
    list_display = ('bot_name', 'channel_name', 'is_enabled')


@admin.register(AliExpressApi)
class AliExpressApiAdmin(admin.ModelAdmin):
    # def has_add_permission(self, request):
    #     if AliExpressApi.objects.all().count() >= 1:
    #         return False
    #     return True
    pass


@admin.register(AmazonApi)
class AmazonApiAdmin(admin.ModelAdmin):
    # def has_add_permission(self, request):
    #     if AmazonApi.objects.all().count() >= 1:
    #         return False
    #     return True
    pass