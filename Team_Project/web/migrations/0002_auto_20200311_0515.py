# Generated by Django 2.2.5 on 2020-03-11 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('videoId', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='game',
            name='game_url',
        ),
        migrations.RemoveField(
            model_name='game',
            name='price',
        ),
        migrations.AddField(
            model_name='game',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='sku',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='game',
            name='game_type',
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Category')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Game')),
            ],
            options={
                'db_table': 'game_tag',
            },
        ),
        migrations.AddField(
            model_name='game',
            name='game_type',
            field=models.ManyToManyField(blank=True, through='web.Tag', to='web.Category'),
        ),
    ]