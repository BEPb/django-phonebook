# Generated by Django 3.2.5 on 2021-07-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0006_auto_20210716_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='militaryunit',
            name='name_unity',
            field=models.CharField(db_index=True, max_length=150, null=True, verbose_name='Наименование в\\ч'),
        ),
        migrations.AlterField(
            model_name='militaryunit',
            name='title',
            field=models.IntegerField(db_index=True, verbose_name='№ в\\ч'),
        ),
    ]
