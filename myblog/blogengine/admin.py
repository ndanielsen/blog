
import models
from django.contrib import admin

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
    	obj.author = request.user
    	obj.save()

admin.site.register(models.Post, PostAdmin)
