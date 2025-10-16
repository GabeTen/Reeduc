from django.contrib import admin
from .models import Course, Activity, UserActivity

admin.site.register(Course)
admin.site.register(Activity)
admin.site.register(UserActivity)
