# Generated by Django 5.0.3 on 2024-03-16 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0012_guide_language_guide_durability_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='id_guide',
            field=models.CharField(max_length=1270, null=True),
        ),
        migrations.AddField(
            model_name='guide',
            name='is_guide',
            field=models.BooleanField(default=False),
        ),
    ]
