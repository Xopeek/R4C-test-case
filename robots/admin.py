from django.contrib import admin

from robots.models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = (
        'model',
        'version'
    )
    search_fields = (
        'model',
        'version'
    )
