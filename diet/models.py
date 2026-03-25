from django.db import models
from django.conf import settings

class MealPlan(models.Model):
    DAYS = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meal_plans')
    day_of_week = models.CharField(max_length=15, choices=DAYS)
    meal_name = models.CharField(max_length=200, default="Daily Plan")
    breakfast = models.CharField(max_length=200, blank=True, null=True)
    lunch = models.CharField(max_length=200, blank=True, null=True)
    dinner = models.CharField(max_length=200, blank=True, null=True)
    snacks = models.CharField(max_length=200, blank=True, null=True)
    calories = models.PositiveIntegerField()
    protein = models.FloatField(help_text="in grams")
    carbs = models.FloatField(help_text="in grams")
    fats = models.FloatField(help_text="in grams")

    def __str__(self):
        return f"{self.user.username} - {self.day_of_week} - {self.meal_name}"

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress_logs')
    date = models.DateField(auto_now_add=True)
    calories_burned = models.PositiveIntegerField(default=0)
    workouts_done = models.PositiveIntegerField(default=0)
    current_weight = models.FloatField(help_text="in kg")
    streak = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s progress on {self.date}"
