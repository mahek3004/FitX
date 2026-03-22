from django.db import models
from django.contrib.auth.models import AbstractUser

class FitnessProfile(AbstractUser):
    FITNESS_GOALS = [
        ('muscle_gain', 'Muscle Gain'),
        ('fat_loss', 'Fat Loss'),
        ('weight_loss', 'Weight Loss'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
    ]
    
    MEMBERSHIP_TYPES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('elite', 'Elite'),
    ]

    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight = models.FloatField(null=True, blank=True, help_text="Current Weight in kg")
    target_weight = models.FloatField(null=True, blank=True, help_text="Target Weight in kg")
    fitness_goal = models.CharField(max_length=50, choices=FITNESS_GOALS, default='muscle_gain')
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES, default='free')
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.username
