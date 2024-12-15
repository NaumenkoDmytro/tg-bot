from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

STATUSES = (
    ("New", "New"),
    ("Approved", "Approved"),
    ("Done", "Done"),
)

API_NAME = (
    ("AliExpress", "AliExpress"),
    ("Amazon", "Amazon")
)

class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True,
        blank=True
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150
    )
    email = models.EmailField(
        _("email address"),
        unique=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class TelegramBotConfig(models.Model):
    class Meta:
        verbose_name = 'Telegram Bot Config'
        verbose_name_plural = 'Telegram Bot Configs'

    bot_name = models.CharField(_('Telegram Bot Name'),
                                max_length=150)
    bot_api_token = models.CharField(_('Telegram Bot API Token'),
                                     max_length=250)
    channel_name = models.CharField(_('Telegram Bot Channel Name'),
                                    max_length=150)
    channel_link = models.CharField(_('Telegram Bot Channel Link'),)
    channel_id = models.CharField(_('Telegram Bot Channel ID'),
                                  max_length=150)
    is_enabled = models.BooleanField(_('Telegram Bot Enabled'),
                                     default=True)

    def __str__(self):
        return f'{self.bot_name} in chanel {self.channel_name}'


class TelegramTestBotConfig(models.Model):
    class Meta:
        verbose_name = 'Telegram Test Bot Config'
        verbose_name_plural = 'Telegram Test Bot Configs'

    bot_name = models.CharField(_('Telegram Test Bot Name'),
                                max_length=150)
    bot_api_token = models.CharField(_('Telegram Test Bot API Token'),
                                     max_length=250)
    channel_name = models.CharField(_('Telegram Test Bot Channel Name'),
                                    max_length=150)
    channel_link = models.CharField(_('Telegram Test Bot Channel Link'),)
    channel_id = models.CharField(_('Telegram Test Bot Channel ID'),
                                  max_length=150)
    is_enabled = models.BooleanField(_('Telegram Test Bot Enabled'),
                                     default=True)

    def __str__(self):
        return f'{self.bot_name} in chanel {self.channel_name}'


class AliExpressApi(models.Model):
    class Meta:
        verbose_name = 'AliExpress API'
        verbose_name_plural = 'AliExpress API'

    name = models.CharField(_('Credential Name'),
                            max_length=150)
    secret_key = models.CharField(_('AliExpress Secret Key'),
                                 max_length=300)
    app_key = models.CharField(_('AliExpress App Key'),
                                max_length=300)
    tracking_id = models.CharField(_('AliExpress Tracking ID'),
                                   max_length=300)

    def __str__(self):
        return self.name


class AmazonApi(models.Model):
    class Meta:
        verbose_name = 'Amazon API'
        verbose_name_plural = 'Amazon API'

    name = models.CharField(_('Credential Name'),
                            max_length=150)
    secret_key = models.CharField(_('Amazon API Secret Key'),
                                  max_length=250)
    access_key = models.CharField(_('Amazon API Access Key'),
                                  max_length=250)
    partner_tag = models.CharField(_('Amazon API Partner Tag'),
                                   max_length=250)

    def __str__(self):
        return f'{self.name}'


class AmazonManualTask(models.Model):
    class Meta:
        verbose_name = 'Amazon Manual Task'
        verbose_name_plural = 'Amazon Manual Tasks'

    name = models.CharField(_('Task Name'),
                            max_length=150)
    status = models.CharField(_('Task Status'),
                              max_length=10,
                              choices=STATUSES,
                              default='New')
    asins = models.JSONField(_('Amazon Products Asins'),
                             default=list,
                             help_text='The field must be empty, for example: [] or contain a list of ASIN\'s in the following JSON format: ["ASIN", "ASIN"].')
    amazon_api = models.ForeignKey(
        AmazonApi,
        on_delete=models.CASCADE,
        verbose_name=_('Amazon API Credentials'),
        related_name='tasks_amazon_api'
    )

    bot = models.ManyToManyField(TelegramBotConfig, verbose_name=_('Telegram Bot Configs'),)

    def __str__(self):
        return f'{self.name}'


class AmazonAutomationTask(models.Model):
    class Meta:
        verbose_name = 'Amazon Automation Task'
        verbose_name_plural = 'Amazon Automation Tasks'

    name = models.CharField(_('Task Name'),
                            max_length=150)
    status = models.CharField(_('Task Status'),
                              max_length=10,
                              choices=STATUSES,
                              default='New')
    keywords = models.CharField(_('KeyWords'),)
    num_items = models.IntegerField(_('Number of Items'),
                                    default=1,
                                    validators=[MinValueValidator(1), MaxValueValidator(10)],
                                    help_text='Min: 1, Max: 10')
    min_price = models.IntegerField(_('Min Price'),
                                    help_text='Filters search results to items with at least one offer price above the specified value. Prices appear in lowest currency denomination. For example, $31.41 should be passed as 3141 or 28.00€ should be 2800.',
                                    default=0)
    max_price = models.IntegerField(_('Max Price'),
                                    help_text='Filters search results to items with at least one offer price above the specified value. Prices appear in lowest currency denomination. For example, $31.41 should be passed as 3141 or 28.00€ should be 2800.',
                                    default=0)
    min_saving_percent = models.PositiveSmallIntegerField(_('Min Savings Percent'),
                                                          help_text="Filters search results to items with at least one offer having saving percentage above the specified value.",
                                                          default=0,
                                                          validators=[MaxValueValidator(100)],)
    min_reviews_rating = models.PositiveSmallIntegerField(_('Min Reviews Rating'),
                                                          help_text="Filters search results to items with customer review ratings above specified value.",
                                                          default=4,
                                                          validators=[MaxValueValidator(5)],)
    start_time = models.DateTimeField(_('Start Time'),
                                      default=timezone.now)

    amazon_api = models.ForeignKey(
        AmazonApi,
        on_delete=models.CASCADE,
        verbose_name=_('Amazon API Credentials'),
        related_name='auto_tasks_amazon_api'
    )

    bot = models.ManyToManyField(TelegramBotConfig, verbose_name=_('Telegram Bot Configs'),)

    def __str__(self):
        return f'{self.name}'


class AmazonSavedProducts(models.Model):
    image = models.CharField()
    image_path = models.CharField()
    product_link = models.CharField()
    title = models.CharField()
    task = models.ForeignKey(AmazonAutomationTask,
                             on_delete=models.CASCADE,
                             related_name='saved_products')


class AliExpressManualTask(models.Model):
    class Meta:
        verbose_name = 'AliExpress Manual Task'
        verbose_name_plural = 'AliExpress Manual Tasks'

    name = models.CharField(_('Task Name'),
                            max_length=150)
    status = models.CharField(_('Task Status'),
                              max_length=10,
                              choices=STATUSES,
                              default='New')
    product_codes = models.JSONField(_('AliExpress Product Codes'),
                             default=list,
                             help_text='The field must be empty, for example: [] or contain a list of product code\'s in the following JSON format: ["CODE", "CODE"].')
    aliexpress_api = models.ForeignKey(
        AliExpressApi,
        on_delete=models.CASCADE,
        verbose_name=_('AliExpress Credentials'),
        related_name='tasks_aliexpress_api'
    )

    bot = models.ManyToManyField(TelegramBotConfig, verbose_name=_('Telegram Bot Configs'),)

    def __str__(self):
        return f'{self.name}'


class AliExpressAutomationTask(models.Model):
    class Meta:
        verbose_name = 'AliExpress Automation Task'
        verbose_name_plural = 'AliExpress Automation Tasks'

    name = models.CharField(_('Task Name'),
                            max_length=150)
    status = models.CharField(_('Task Status'),
                              max_length=10,
                              choices=STATUSES,
                              default='New')
    keywords = models.CharField(_('KeyWords'),)
    num_items = models.IntegerField(_('Number of Items'),
                                    default=1,
                                    validators=[MinValueValidator(1), MaxValueValidator(10)],
                                    help_text='Min: 1, Max: 10')
    min_price = models.IntegerField(_('Min Price'),
                                    help_text='Filters search results to items with at least one offer price above the specified value. Prices appear in lowest currency denomination. For example, $31.41 should be passed as 3141 or 28.00€ should be 2800.',
                                    default=0)
    max_price = models.IntegerField(_('Max Price'),
                                    help_text='Filters search results to items with at least one offer price above the specified value. Prices appear in lowest currency denomination. For example, $31.41 should be passed as 3141 or 28.00€ should be 2800.',
                                    default=0)
    delivery_days = models.PositiveSmallIntegerField(_('Delivery Days'),
                                                    default=0,
                                                    validators=[MaxValueValidator(100)],)
    start_time = models.DateTimeField(_('Start Time'),
                                      default=timezone.now)

    aliexpress_api = models.ForeignKey(
        AliExpressApi,
        on_delete=models.CASCADE,
        verbose_name=_('AliExpress API Credentials'),
        related_name='auto_tasks_aliexpress_api'
    )

    bot = models.ManyToManyField(TelegramBotConfig, verbose_name=_('Telegram Bot Configs'),)

    def __str__(self):
        return f'{self.name}'
