# Generated by Django 3.1.7 on 2021-04-24 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='CATDesc',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='CATImg',
            field=models.ImageField(null=True, upload_to='category/', verbose_name='Image'),
        ),
    ]
