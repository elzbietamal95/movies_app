# Generated by Django 2.2.10 on 2020-02-17 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0019_auto_20200217_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='first_name',
            field=models.CharField(help_text='Required.', max_length=50, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='director',
            name='last_name',
            field=models.CharField(help_text='Required.', max_length=150, verbose_name='last name'),
        ),
    ]
