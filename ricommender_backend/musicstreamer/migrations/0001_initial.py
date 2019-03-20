# Generated by Django 2.1.7 on 2019-03-20 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=255, verbose_name='File')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('artist', models.CharField(max_length=255, verbose_name='Artist')),
                ('album', models.CharField(max_length=255, verbose_name='Album')),
            ],
        ),
    ]