from django.contrib import admin
from . import models

admin.site.register(models.Context)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.TopicNames)
admin.site.register(models.Topics)
admin.site.register(models.TrainedModel)
admin.site.register(models.Prediction)