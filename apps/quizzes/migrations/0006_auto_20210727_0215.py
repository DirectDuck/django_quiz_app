# Generated by Django 3.2.5 on 2021-07-26 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0005_auto_20210727_0056'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField()),
                ('text', models.CharField(blank=True, max_length=65)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='quizzes.quiz')),
            ],
        ),
        migrations.AddConstraint(
            model_name='quizresult',
            constraint=models.UniqueConstraint(fields=('quiz', 'score'), name='unique_quiz_score'),
        ),
    ]
