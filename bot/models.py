from django.db import models
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
class BotSettings(models.Model):
    token = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255)

    def __str__(self):
        return f'Bot Settings'
class Users(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    language = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.user_id}'

class language(models.Model):
    language_code = models.CharField(max_length=127)
    text_welcome = models.TextField(max_length=1500)
    find_tour = models.CharField(max_length=127, null=True)
    imguider = models.CharField(max_length=127, null=True)
    contact_menu = models.CharField(max_length=127, null=True)
    contact_text = models.CharField(max_length=127, null=True)
    months = models.JSONField(default=list)
    days = models.JSONField(default=list)
    choose_day = models.CharField(max_length=1270, null=True)
    back = models.CharField(max_length=1270, null=True)
    share_contant = models.CharField(max_length=1270, null=True)
    guide_name = models.CharField(max_length=1270, null=True)
    guide_license = models.CharField(max_length=1270, null=True)
    guide_language = models.CharField(max_length=1270, null=True)
    guide_price = models.CharField(max_length=1270, null=True)
    guide_durability = models.CharField(max_length=1270, null=True)
    guide_photo = models.CharField(max_length=1270, null=True)
    guide_number = models.CharField(max_length=1270, null=True)
    ad = models.CharField(max_length=1270, null=True)

    def __str__(self):
        return f'Language'

class guide(models.Model):
    id_guide = models.CharField(max_length=1270, null=True)
    is_guide = models.BooleanField(default=False)
    name = models.CharField(max_length=1270, null=True)
    license = models.ImageField(blank=True, upload_to='photos/')
    language = models.CharField(max_length=1270, null=True)
    price = models.CharField(max_length=1270, null=True)
    durability = models.CharField(max_length=1270, null=True)
    photo = models.ImageField(blank=True, upload_to='photos/')
    number = models.CharField(max_length=1270, null=True)

    def __str__(self):
        return f'{self.name}'
