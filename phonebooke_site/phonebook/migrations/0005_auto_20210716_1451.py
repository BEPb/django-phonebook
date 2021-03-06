# Generated by Django 3.2.5 on 2021-07-16 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0004_auto_20210716_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='Наименование подразделения')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
                'ordering': ['id'],
            },
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='division',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='phonebook.division', verbose_name='Подразделение'),
        ),
    ]
