from django.contrib import admin
from ihr_api import models


admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.Color)
admin.site.register(models.Size)
admin.site.register(models.User)
admin.site.register(models.Store)