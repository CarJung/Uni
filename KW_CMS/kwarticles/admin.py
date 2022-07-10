from django.contrib import admin
from django.db import models
from kwarticles.models import KWarticles, KWComment
# Register your models here.\

modules = [KWarticles, KWComment]
admin.site.register(modules)