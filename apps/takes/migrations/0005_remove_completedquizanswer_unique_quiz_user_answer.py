# Generated by Django 3.2.5 on 2021-08-09 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('takes', '0004_completedquizanswer_unique_quiz_user_answer'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='completedquizanswer',
            name='unique_quiz_user_answer',
        ),
    ]
