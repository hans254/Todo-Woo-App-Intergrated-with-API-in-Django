from django.contrib import admin
from .models import todowooApp

# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(todowooApp, TodoAdmin)
