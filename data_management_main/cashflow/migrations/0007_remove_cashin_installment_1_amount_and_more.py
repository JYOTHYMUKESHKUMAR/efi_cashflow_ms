# Generated by Django 5.0.5 on 2024-05-08 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0006_expensesource_incomesource_project_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashin',
            name='installment_1_amount',
        ),
        migrations.RemoveField(
            model_name='cashin',
            name='installment_1_date',
        ),
        migrations.RemoveField(
            model_name='cashin',
            name='installment_2_amount',
        ),
        migrations.RemoveField(
            model_name='cashin',
            name='installment_2_date',
        ),
        migrations.RemoveField(
            model_name='cashin',
            name='installment_3_amount',
        ),
        migrations.RemoveField(
            model_name='cashin',
            name='installment_3_date',
        ),
        migrations.RemoveField(
            model_name='cashin',
            name='installment_4_amount',
        ),
        migrations.RemoveField(
            model_name='cashin',
            name='installment_4_date',
        ),
        migrations.RemoveField(
            model_name='cashin',
            name='num_installments',
        ),
        migrations.AddField(
            model_name='expensesource',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='expensesource',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='incomesource',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='incomesource',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
