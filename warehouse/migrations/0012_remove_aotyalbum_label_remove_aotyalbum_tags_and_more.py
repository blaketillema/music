# Generated by Django 4.2.2 on 2023-06-24 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0011_alter_aotyalbum_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aotyalbum',
            name='label',
        ),
        migrations.RemoveField(
            model_name='aotyalbum',
            name='tags',
        ),
        migrations.AlterField(
            model_name='aotyalbumrating',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='warehouse.aotyalbum'),
        ),
    ]
