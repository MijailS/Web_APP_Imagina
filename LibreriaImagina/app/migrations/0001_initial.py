# Generated by Django 4.2.1 on 2023-06-07 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=254)),
                ('tipo_consulta', models.IntegerField(choices=[[0, 'a'], [1, 'b'], [2, 'c'], [4, 'd']])),
                ('mensaje', models.TextField()),
                ('avisos', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('ID_LIBRO', models.IntegerField(primary_key=True, serialize=False)),
                ('ISBN', models.IntegerField()),
                ('TITULO', models.CharField(max_length=200)),
                ('VALOR', models.IntegerField()),
                ('PAGINAS', models.IntegerField()),
                ('STOCK', models.IntegerField()),
                ('IMG', models.CharField(max_length=500)),
                ('AUTOR', models.CharField(max_length=70)),
                ('ANIO_EDICION', models.IntegerField()),
                ('RESENIA', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'app_libro',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
                ('categoria', models.CharField(max_length=32)),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('id_tecnico', models.AutoField(db_column='ID_TECNICO', primary_key=True, serialize=False)),
                ('nombre_completo', models.CharField(db_column='NOMBRE_COMPLETO', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id_visita', models.AutoField(db_column='ID_VISITA', primary_key=True, serialize=False)),
                ('fecha', models.DateField(db_column='FECHA')),
                ('hora', models.TimeField(db_column='HORA')),
                ('descripcion', models.CharField(db_column='DESCRIPCION', max_length=500)),
                ('tecnico', models.ForeignKey(db_column='TECNICO_ID_TECNICO', on_delete=django.db.models.deletion.CASCADE, to='app.tecnico')),
            ],
        ),
    ]