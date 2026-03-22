from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('blog/', views.blog, name='blog'),
    path('community/', views.community, name='community'),
    path('contact/', views.contact, name='contact'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('success_stories/', views.success_stories),  # alias
    path('story/', views.story_detail, name='story_detail'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('faq/', views.faq_page, name='faq'),
]
