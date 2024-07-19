# Generated by Django 5.0.6 on 2024-07-19 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_payment_card_number_alter_payment_cvc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='card_number',
            field=models.CharField(max_length=16, verbose_name='Card number'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='cvc',
            field=models.CharField(max_length=3, verbose_name='CVC'),
        ),
    ]