from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Challenge, Testimonial, SuccessStory, FAQ
from workout.models import Trainer, WorkoutProgram

# Dummy testimonial data for when DB is empty
DUMMY_TESTIMONIALS = [
    {
        'name': 'Rahul Sharma',
        'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&q=80',
        'text': 'FitX completely transformed my life. I lost 22kg in 6 months with their personalized training program. The coaches are world-class and the community is incredibly supportive!',
        'rating': 5,
        'role': 'Lost 22kg in 6 Months',
    },
    {
        'name': 'Priya Mehta',
        'avatar': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80',
        'text': 'The diet plan generator is phenomenal. I finally understand what my body needs. I went from feeling exhausted to running 10km every morning. FitX literally saved my health.',
        'rating': 5,
        'role': 'Marathon Runner Now',
    },
    {
        'name': 'Arjun Kapoor',
        'avatar': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80',
        'text': 'Best investment I ever made in myself. The workout library is massive and the exercise detail pages with videos make it so easy to learn proper form. Gained 8kg of pure muscle!',
        'rating': 5,
        'role': 'Gained 8kg Lean Muscle',
    },
    {
        'name': 'Sneha Patel',
        'avatar': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&q=80',
        'text': 'FitX\'s HIIT programs are incredibly well-designed. I went from zero fitness to completing a 30-day shred challenge. The progress tracking feature keeps me motivated every single day.',
        'rating': 4,
        'role': '30-Day Shred Champion',
    },
    {
        'name': 'Vikram Singh',
        'avatar': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&q=80',
        'text': 'As a busy professional, I love that I can track everything from the dashboard. The routine builder helped me stay consistent even with a packed schedule. Down 15kg and never felt better!',
        'rating': 5,
        'role': 'Consistent for 8 Months',
    },
]

def index(request):
    featured_trainers = Trainer.objects.all()[:6]
    workout_programs = WorkoutProgram.objects.all()[:4]
    latest_blog = BlogPost.objects.all().order_by('-created_at')[:3]
    testimonials = Testimonial.objects.all().order_by('-created_at')[:5]
    faqs = FAQ.objects.all()

    if not faqs.exists():
        FAQ.objects.create(question="What makes FitX different from other gyms?", answer="FitX is not just a gym; it's a holistic fitness ecosystem with world-class facilities, nutrition coaching, mental wellness programs, and a vibrant community.", order=1)
        FAQ.objects.create(question="Can I access multiple centers with one membership?", answer="Yes! Our 'FitX Elite' plan gives you seamless access to every FitX center and partner gym across the country.", order=2)
        FAQ.objects.create(question="Are personal trainers available?", answer="Absolutely. We have a team of elite, certified trainers specialized in bodybuilding, CrossFit, Yoga, and athletic conditioning.", order=3)
        FAQ.objects.create(question="Do you have a mobile app?", answer="Yes, the FitX app is available on both iOS and Android. You can book classes, track nutrition, and monitor progress on the go.", order=4)
        FAQ.objects.create(question="Is there a trial period available?", answer="Yes, we offer a 3-day complimentary pass for all first-time visitors to experience our facilities and a few classes.", order=5)
        FAQ.objects.create(question="What are your opening hours?", answer="Most of our premium centers are open 24/7. Standard centers usually operate from 5:00 AM to 11:00 PM.", order=6)
        FAQ.objects.create(question="Do you offer student discounts?", answer="Yes, we have special membership rates for students under 25 with a valid ID card. Check our pricing section for details.", order=7)
        faqs = FAQ.objects.all()

    return render(request, 'core/index.html', {
        'trainers': featured_trainers,
        'programs': workout_programs,
        'blog_posts': latest_blog,
        'testimonials': testimonials,
        'dummy_testimonials': DUMMY_TESTIMONIALS,
        'faqs': faqs
    })

def blog(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'core/blog.html', {'posts': posts})

def community(request):
    challenges = Challenge.objects.all()
    return render(request, 'core/community.html', {'challenges': challenges})

def contact(request):
    return render(request, 'core/contact.html')

def success_stories(request):
    stories = SuccessStory.objects.all().order_by('-created_at')
    
    # Optional: Seed data if empty (only for dev convenience)
    if not stories.exists():
        initial_stories = [
            {
                'name': 'Mike Roberts', 
                'result_stat': '40 Kg Weight Loss', 
                'image_url': 'https://images.unsplash.com/photo-1549476464-37392f717541?w=600&q=80', 
                'brief': 'Switched from severe fast food to the FitX Lean Muscle program.',
                'full_story': 'Mike was struggling with his health and energy levels for years. After joining FitX, he followed a strict ketogenic diet combined with heavy resistance training. Within 12 months, he transformed his physique and now competes in local amateur powerlifting events.',
                'is_gain': False
            },
            {
                'name': 'Sarah Jenkins', 
                'result_stat': '8 Kg Muscle Gain', 
                'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&q=80', 
                'brief': 'Focused on high-protein intake and heavy compound lifting.',
                'full_story': 'Sarah was always naturally thin but lacked strength. She started our "Elite Hypertrophy" program and tripled her caloric intake with healthy, whole foods. Her dedication to progressive overload has made her an inspiration in our community.',
                'is_gain': True
            },
        ]
        for s in initial_stories:
            SuccessStory.objects.get_or_create(**s)
        stories = SuccessStory.objects.all().order_by('-created_at')

    return render(request, 'account/success.html', {'stories_list': stories})

def story_detail(request):
    story_id = request.GET.get('id')
    story = get_object_or_404(SuccessStory, id=story_id) if story_id else SuccessStory.objects.first()
    return render(request, 'core/story.html', {'story': story})

def about(request):
    return render(request, 'core/about.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def terms(request):
    return render(request, 'core/terms.html')

def faq_page(request):
    faqs = FAQ.objects.all()
    return render(request, 'core/faq.html', {'faqs': faqs})
