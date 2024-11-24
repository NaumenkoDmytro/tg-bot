from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

STATUSES = (
    ("New", "New"),
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

    bot_name = models.CharField(_('Telegram Bot Name'), max_length=150)
    bot_api_token = models.CharField(_('Telegram Bot API Token'), max_length=250)
    channel_name = models.CharField(_('Telegram Bot Channel Name'), max_length=150)
    channel_id = models.CharField(_('Telegram Bot Channel ID'), max_length=150)
    is_enabled = models.BooleanField(_('Telegram Bot Enabled'), default=True)

    def __str__(self):
        return f'{self.bot_name} in chanel {self.channel_name}'


class Task(models.Model):
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Task'

    name = models.CharField(_('Task Name'), max_length=150)
    status = models.CharField(_('Task Status'), max_length=10, choices=STATUSES, default='New')
    start_time = models.DateTimeField(_('Start Time'), default=timezone.now)
    api_name = models.CharField(_('API Name'), max_length=15, choices=API_NAME)

    def __str__(self):
        return f'{self.name}'


class AliExpressApi(models.Model):
    class Meta:
        verbose_name = 'AliExpress API'
        verbose_name_plural = 'AliExpress API'

    api_token = models.CharField(_('AliExpress API Token'), max_length=250)

    def __str__(self):
        return f'AliExpress API'


class AmazonApi(models.Model):
    class Meta:
        verbose_name = 'Amazon API'
        verbose_name_plural = 'Amazon API'

    secret_key = models.CharField(_('Amazon API Secret Key'), max_length=250)
    access_key = models.CharField(_('Amazon API Access Key'), max_length=250)
    partner_tag = models.CharField(_('Amazon API Partner Tag'), max_length=250)
    country = models.CharField(_('Amazon API Country'), max_length=5)

    def __str__(self):
        return f'{self.partner_tag}'
