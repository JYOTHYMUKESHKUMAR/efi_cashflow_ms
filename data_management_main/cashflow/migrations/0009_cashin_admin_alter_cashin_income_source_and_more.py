# Generated by Django 5.0.5 on 2024-05-08 21:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0008_rename_expense_source_list_expensesource_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashin',
            name='admin',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cashin',
            name='income_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cashflow.incomesource'),
        ),
        migrations.AlterField(
            model_name='cashin',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cashflow.project'),
        ),
    ]
