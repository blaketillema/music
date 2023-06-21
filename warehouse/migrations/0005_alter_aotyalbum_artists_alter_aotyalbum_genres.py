# Generated by Django 4.2.2 on 2023-06-18 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_alter_aotyalbum_artists_remove_aotyalbum_genres_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aotyalbum',
            name='artists',
            field=models.ManyToManyField(to='warehouse.aotyartist'),
        ),
        migrations.AlterField(
            model_name='aotyalbum',
            name='genres',
            field=models.ManyToManyField(to='warehouse.aotygenre'),
        ),
    ]