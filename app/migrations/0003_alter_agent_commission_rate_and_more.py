# Generated by Django 5.2.1 on 2025-05-27 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_agent_commission_rate_agent_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='Commission_rate',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='agent',
            name='Total_commission',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='agent',
            name='total_sales',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
