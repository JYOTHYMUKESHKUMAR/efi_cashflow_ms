# Generated by Django 5.0.5 on 2024-05-08 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0004_alter_customuser_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_source', models.CharField(blank=True, choices=[('source1', 'Source 1'), ('source2', 'Source 2')], max_length=250)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Received', 'Received'), ('Scheduled', 'Scheduled')], default='Received', max_length=50)),
                ('remark', models.TextField(blank=True)),
                ('cash_in', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('project', models.CharField(blank=True, max_length=250)),
                ('cost_center', models.CharField(choices=[('catalyst', 'Catalyst'), ('oil_and_gas', 'Oil and Gas'), ('general_chemicals', 'General Chemicals'), ('overhead', 'Overhead')], default='catalyst', max_length=50)),
                ('service_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
