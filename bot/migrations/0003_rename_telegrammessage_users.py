# Generated by Django 5.0.3 on 2024-03-08 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_rename_text_telegrammessage_first_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TelegramMessage',
            new_name='Users',
        ),
    ]
