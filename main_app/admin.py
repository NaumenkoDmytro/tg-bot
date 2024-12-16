from django.contrib import admin
from django import forms
from .models import (User, TelegramBotConfig, AliExpressApi, AmazonApi, AmazonManualTask, AmazonAutomationTask,
                     AliExpressManualTask, AliExpressAutomationTask, TelegramTestBotConfig, AmazonSavedProducts,
                     AliExpressSavedProducts)
from .utils.amazon_manual_task_process import amazon_manual_process
from .utils.aliexpress_manual_task_process import ali_manual_process
from .utils.amazon_alik_post_to_test_chanel import amazon, alik

admin.site.register(User)
# admin.site.register(AmazonSavedProducts)
admin.site.register(AliExpressSavedProducts)

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


class AliExpressManualTaskForm(forms.ModelForm):
    class Meta:
        model = AliExpressManualTask
        fields = '__all__'

    bot = forms.ModelMultipleChoiceField(
        queryset=TelegramBotConfig.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def clean_asins(self):
        product_codes = self.cleaned_data['product_codes']

        if not type(product_codes) is list:
            self.add_error(
                "product_codes",
                "The field must be empty, for example: [] or contain a list "
                'of product code\'s in the following JSON format: ["CODE", "CODE"].',
            )

        return product_codes


@admin.register(AmazonManualTask)
class AmazonManualTaskAdmin(admin.ModelAdmin):
    form = AmazonManualTaskModelForm
    list_display = ('name', 'status')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        amazon_manual_process(obj)


@admin.register(AliExpressManualTask)
class AliExpressManualTaskAdmin(admin.ModelAdmin):
    form = AliExpressManualTaskForm
    list_display = ('name', 'status')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        ali_manual_process(obj=obj)


class AmazonAutoTaskModelForm(forms.ModelForm):
    class Meta:
        model = AmazonAutomationTask
        fields = '__all__'

    def clean_num_items(self):
        value = self.cleaned_data['num_items']
        if value < 1 or value > 10:
            raise forms.ValidationError('Value must be between 1 and 10.')
        return value

    def clean_min_saving_percent(self):
        value = self.cleaned_data['min_saving_percent']
        if value > 100:
            raise forms.ValidationError('Value must be less then 100.')
        return value

    def clean_min_reviews_rating(self):
        value = self.cleaned_data['min_reviews_rating']
        if value > 5:
            raise forms.ValidationError('Value must be less then 5.')
        return value


class AliExpressAutoTaskModelForm(forms.ModelForm):
    class Meta:
        model = AliExpressAutomationTask
        fields = '__all__'

    def clean_num_items(self):
        value = self.cleaned_data['num_items']
        if value < 1 or value > 10:
            raise forms.ValidationError('Value must be between 1 and 10.')
        return value

    def clean_delivery_days(self):
        value = self.cleaned_data['delivery_days']
        if value > 100:
            raise forms.ValidationError('Value must be less then 100.')
        return value

    def clean_min_saving_percent(self):
        value = self.cleaned_data['min_saving_percent']
        if value > 100:
            raise forms.ValidationError('Value must be less then 100.')
        return value

    def clean_min_reviews_rating(self):
        value = self.cleaned_data['min_reviews_rating']
        if value > 5:
            raise forms.ValidationError('Value must be less then 5.')
        return value


@admin.register(AliExpressAutomationTask)
class AliExpressAutoTaskAdmin(admin.ModelAdmin):
    form = AliExpressAutoTaskModelForm
    list_display = ('name', 'status', 'keywords', 'start_time')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        alik(obj)


@admin.register(AmazonAutomationTask)
class AmazonAutoTaskAdmin(admin.ModelAdmin):
    form = AmazonAutoTaskModelForm
    list_display = ('name', 'status', 'keywords', 'start_time')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        amazon(obj)


@admin.register(TelegramBotConfig)
class TelegramBotConfigAdmin(admin.ModelAdmin):
    list_display = ('bot_name', 'channel_name', 'is_enabled')


@admin.register(TelegramTestBotConfig)
class TelegramTestBotConfigAdmin(admin.ModelAdmin):
    list_display = ('bot_name', 'channel_name', 'is_enabled')

    def has_add_permission(self, request):
        if TelegramTestBotConfig.objects.all().count() >= 1:
            return False
        return True


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