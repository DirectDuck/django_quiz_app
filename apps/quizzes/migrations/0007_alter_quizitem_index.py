# Generated by Django 3.2.5 on 2021-07-28 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0006_auto_20210727_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizitem',
            name='index',
            field=models.PositiveIntegerField(db_index=True),
        ),
    ]