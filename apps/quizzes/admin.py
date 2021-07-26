from django.contrib import admin

from . import models


admin.site.register(models.Quiz)
admin.site.register(models.QuizItem)
admin.site.register(models.QuizItemAnswer)
