from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FitnessProfile

@receiver(post_save, sender=FitnessProfile)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Since FitnessProfile is the custom user model (AbstractUser), 
    this signal is less about creating a separate profile object 
    and more about ensuring any post-creation logic is handled if needed.
    However, the prompt asks for a signal to automatically create a FitnessProfile.
    If they meant a separate Profile model, it would apply there.
    Since we are using AbstractUser, the instance IS the profile.
    
    If we were to add a related model like 'UserStats', we would do it here.
    """
    if created:
        # Example: Log new user creation or set defaults if not handled by model
        pass

@receiver(post_save, sender=FitnessProfile)
def save_user_profile(sender, instance, **kwargs):
    # Logic to run on every save
    pass
