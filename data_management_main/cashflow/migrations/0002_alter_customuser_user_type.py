# Generated by Django 5.0.5 on 2024-05-07 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('ACCOUNT_TEAM', 'ACCOUNT')], default='ACCOUNT_TEAM', max_length=50),
        ),
    ]
