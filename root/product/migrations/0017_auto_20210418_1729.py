# Generated by Django 3.2 on 2021-04-18 17:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_merge_0014_auto_20210417_1652_0015_auto_20210416_2301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ownerproduct',
            old_name='OwnerProduct',
            new_name='Ownerproduct',
        ),
        migrations.AlterField(
            model_name='ownerproduct',
            name='OwnerQuantity',
            field=models.IntegerField(default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]