# Generated by Django 4.2.1 on 2023-06-14 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoTarjeta',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
                ('numero_tarjeta', models.IntegerField()),
                ('cvv', models.IntegerField()),
                ('fecha_vencimiento', models.CharField(max_length=5)),
            ],
        ),
    ]
