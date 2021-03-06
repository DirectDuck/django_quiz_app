# Generated by Django 3.2.5 on 2021-07-26 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0004_auto_20210726_0726'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name_plural': 'Quizzes'},
        ),
        migrations.RemoveConstraint(
            model_name='quizitem',
            name='unique_quiz_questions',
        ),
        migrations.AlterField(
            model_name='quiz',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Review'), (3, 'Rejected'), (4, 'Approved')], default=1),
        ),
    ]
