# Generated by Django 3.0.5 on 2020-04-19 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200419_0744'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('note', models.TextField(max_length=6000)),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
