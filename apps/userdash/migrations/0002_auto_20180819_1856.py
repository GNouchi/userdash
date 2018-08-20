# Generated by Django 2.1 on 2018-08-20 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdash', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_level',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
