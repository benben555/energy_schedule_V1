# Generated by Django 3.1.2 on 2023-12-20 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumers',
            name='status',
            field=models.CharField(default='未参与本轮调度', max_length=128, verbose_name='当前状态'),
        ),
    ]
