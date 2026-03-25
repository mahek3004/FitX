from django.db import models
from django.conf import settings

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog/', null=True, blank=True)

    def __str__(self):
        return self.title

class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    reward = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.user.username}"


class SuccessStory(models.Model):
    name = models.CharField(max_length=100)
    result_stat = models.CharField(max_length=100) # e.g. "40 Kg Weight Loss"
    image = models.ImageField(upload_to='stories/', null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True) # Fallback for now
    before_image = models.ImageField(upload_to='stories/before/', null=True, blank=True)
    after_image = models.ImageField(upload_to='stories/after/', null=True, blank=True)
    brief = models.TextField()
    full_story = models.TextField(blank=True, default='')
    is_gain = models.BooleanField(default=False) # True for muscle gain, False for loss
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    topic = models.CharField(max_length=100)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.topic}"
