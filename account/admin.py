from django.contrib import admin
from .models import FitnessProfile

@admin.register(FitnessProfile)
class FitnessProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fitness_goal', 'membership_type')
    list_filter = ('fitness_goal', 'membership_type')
    search_fields = ('username', 'email')
