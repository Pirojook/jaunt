# Generated by Django 5.0.3 on 2024-03-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0021_alter_guide_photo_g'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='license_g',
            field=models.ImageField(blank=True, upload_to='E:\\Python\\jaunt\\media\\media'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='photo_g',
            field=models.ImageField(blank=True, upload_to='E:\\Python\\jaunt\\media\\media'),
        ),
    ]