# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-18 13:07
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20180718_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='price',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0.0'), default_currency='USD', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='subjobs',
            name='price',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0.0'), default_currency='USD', max_digits=10, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='jobs',
            unique_together=set([('item', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='subjobs',
            unique_together=set([('subitem', 'number')]),
        ),
    ]