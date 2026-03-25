from django.contrib import admin
from .models import MealPlan, UserProgress

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'meal_name', 'calories')
    list_filter = ('day_of_week',)
    search_fields = ('user__username', 'meal_name')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'current_weight', 'calories_burned')
    list_filter = ('date',)
    search_fields = ('user__username',)
