# Generated by Django 2.1.7 on 2020-03-09 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vue_shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.ManyToManyField(blank=True, to='vue_shop.Roles', verbose_name='角色'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='username',
            field=models.CharField(max_length=64, unique=True, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='roles',
            name='permission',
            field=models.ManyToManyField(blank=True, to='vue_shop.Permission', verbose_name='权限'),
        ),
    ]