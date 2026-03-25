from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import random
from .models import FitnessProfile, OTPVerification
from diet.models import UserProgress, MealPlan
from workout.models import WorkoutProgram, UserRoutine
from core.models import Challenge
import json
from django.core.serializers.json import DjangoJSONEncoder

@login_required
def dashboard(request):
    progress_data = UserProgress.objects.filter(user=request.user).order_by('date')
    workouts = WorkoutProgram.objects.all()[:6]
    diet_plans = MealPlan.objects.filter(user=request.user)
    challenges = Challenge.objects.all()[:6]
    
    # If no meal plans for user, get some default ones or show message
    if not diet_plans.exists():
        diet_plans = None
        
    routines = UserRoutine.objects.filter(user=request.user).select_related('exercise')
    total_routine_calories = sum(r.exercise.calories_burned for r in routines)
    
    # Calculate Sums
    from django.db.models import Sum
    total_workouts = UserProgress.objects.filter(user=request.user).aggregate(Sum('workouts_done'))['workouts_done__sum'] or 0
    total_calories = UserProgress.objects.filter(user=request.user).aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    streak = progress_data.last().streak if progress_data.exists() else 0
    current_weight = request.user.weight or (progress_data.last().current_weight if progress_data.exists() else 0)

    # Prepare data for Chart.js
    labels = [p.date.strftime("%b %d") for p in progress_data]
    calories = [p.calories_burned for p in progress_data]
    weights = [float(p.current_weight) for p in progress_data]
    
    target_weight = request.user.target_weight or 0
    weight_to_goal = current_weight - target_weight if target_weight else 0
    
    # sessions this week
    from datetime import timedelta, date
    start_of_week = date.today() - timedelta(days=date.today().weekday())
    sessions_this_week = UserProgress.objects.filter(user=request.user, date__gte=start_of_week, workouts_done__gt=0).count()
    session_goal = 5
    session_percent = min(100, int((sessions_this_week / session_goal) * 100)) if session_goal > 0 else 0

    # Goal Percentages
    calorie_goal = 2500
    calorie_percent = min(100, int((total_routine_calories / calorie_goal) * 100)) if calorie_goal > 0 else 0

    context = {
        'progress_json': json.dumps({
            'labels': labels,
            'calories': calories,
            'weights': weights
        }, cls=DjangoJSONEncoder),
        'latest_progress': progress_data.last(),
        'total_workouts': total_workouts,
        'total_calories': total_calories,
        'streak': streak,
        'current_weight': current_weight,
        'target_weight': target_weight,
        'weight_to_goal': weight_to_goal,
        'sessions_this_week': sessions_this_week,
        'session_goal': session_goal,
        'session_percent': session_percent,
        'calorie_goal': calorie_goal,
        'calorie_percent': calorie_percent,
        'workouts': workouts,
        'diet_plans': diet_plans,
        'challenges': challenges,
        'routines': routines,
        'total_routine_calories': total_routine_calories,
    }
    return render(request, 'account/dashboard.html', context)

@login_required
def log_progress(request):
    from datetime import date
    if request.method == 'POST':
        weight = float(request.POST.get('weight', 0))
        target_weight = request.POST.get('target_weight')
        calories = int(request.POST.get('calories_burned', 0))
        workouts = int(request.POST.get('workouts_done', 1))
        
        # Update user profile weights
        user = request.user
        user.weight = weight
        if target_weight:
            user.target_weight = float(target_weight)
        user.save()

        progress = UserProgress.objects.filter(user=request.user, date=date.today()).first()
        if progress:
            progress.current_weight = weight
            progress.calories_burned += calories
            progress.workouts_done += workouts
            progress.save()
        else:
            UserProgress.objects.create(
                user=request.user,
                date=date.today(),
                current_weight=weight,
                calories_burned=calories,
                workouts_done=workouts,
                streak=1 # Basic placeholder for streak
            )
        messages.success(request, "Progress logged successfully!")
    return redirect('dashboard')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validation
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'account/signup.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'account/signup.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'account/signup.html')
        
        if FitnessProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose another.')
            return render(request, 'account/signup.html')
        
        if email and FitnessProfile.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'account/signup.html')
        
        # Create user
        user = FitnessProfile.objects.create_user(
            username=username, 
            email=email, 
            password=password
        )
        login(request, user)
        messages.success(request, f'Welcome to FitX, {username}! 🎉')
        
        if user.email == 'maheksavaliya3004@gmail.com' and user.username == 'MAHEK':
            return redirect('admin_dashboard')
        return redirect('home')
    
    return render(request, 'account/signup.html')

def verify_otp(request):
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        messages.error(request, 'No pending OTP verification.')
        return redirect('login')
        
    user = get_object_or_404(FitnessProfile, id=user_id)
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()
        
        # Check if OTP exists and is valid (not older than 5 mins)
        verification = OTPVerification.objects.filter(user=user, otp=otp_entered).last()
        
        if verification:
            time_diff = timezone.now() - verification.created_at
            if time_diff.total_seconds() <= 300: # 5 minutes
                # Valid OTP!
                login(request, user)
                del request.session['pre_otp_user_id']
                OTPVerification.objects.filter(user=user).delete() # clean up
                
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Check for "next" parameter
                next_url = request.session.pop('post_login_next', '')
                if next_url:
                    return redirect(next_url)
                    
                if user.email == 'maheksavaliya3004@gmail.com' and user.username == 'MAHEK':
                    return redirect('admin_dashboard')
                return redirect('home')
            else:
                messages.error(request, 'OTP has expired. Please login again.')
                del request.session['pre_otp_user_id']
                return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            
    return render(request, 'account/otp_verify.html', {'email': user.email})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            # Generate OTP
            otp_code = str(random.randint(100000, 999999))
            
            # Save OTP
            OTPVerification.objects.filter(user=user).delete() # remove old ones
            OTPVerification.objects.create(user=user, otp=otp_code)
            
            # Send Email
            try:
                send_mail(
                    'FitX Login OTP Verification',
                    f'Your OTP for FitX login is: {otp_code}\nThis OTP is valid for 5 minutes.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print("Email sending failed:", e)
                # Fallback to display message for testing if SMTP fails
                messages.info(request, f'DEVELOPMENT MODE: Your OTP is {otp_code}')
            
            # Store ID in session and redirect to verify page
            request.session['pre_otp_user_id'] = user.id
            if request.GET.get('next'):
                request.session['post_login_next'] = request.GET.get('next')
                
            return redirect('verify_otp')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.age = request.POST.get('age') or None
        user.height = request.POST.get('height') or None
        user.weight = request.POST.get('weight') or None
        user.fitness_goal = request.POST.get('fitness_goal', 'muscle_gain')
        
        # Handle profile image
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('dashboard')
    return redirect('dashboard')


# ─── Frontend Admin Dashboard ─────────────────────────────────────────────────

def admin_dashboard(request):
    """Custom frontend admin dashboard for staff/superusers."""
    if request.user.email != 'maheksavaliya3004@gmail.com' or request.user.username != 'MAHEK':
        messages.error(request, "Access denied. Only specific admins can view this page.")
        return redirect('login')
    from store.models import Payment, MembershipPlan
    from django.db.models import Sum, Count

    users = FitnessProfile.objects.all().order_by('-date_joined')
    meal_plans = MealPlan.objects.select_related('user').order_by('-id')[:50]
    workout_programs = WorkoutProgram.objects.all()
    payments = Payment.objects.select_related('user').order_by('-created_at')[:50]
    routines = UserRoutine.objects.select_related('user', 'exercise').order_by('-id')[:30]

    # Stats
    total_users = users.count()
    total_payments = payments.count()
    total_revenue = Payment.objects.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0
    total_meal_plans = MealPlan.objects.count()

    context = {
        'users': users,
        'meal_plans': meal_plans,
        'workout_programs': workout_programs,
        'payments': payments,
        'routines': routines,
        'total_users': total_users,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
        'total_meal_plans': total_meal_plans,
    }
    return render(request, 'account/admin_dashboard.html', context)


def admin_delete_user(request, user_id):
    if request.user.email != 'maheksavaliya3004@gmail.com' or request.user.username != 'MAHEK':
        return redirect('login')
    user = get_object_or_404(FitnessProfile, id=user_id)
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('admin_dashboard')
    username = user.username
    user.delete()
    messages.success(request, f"User '{username}' deleted successfully.")
    return redirect('admin_dashboard')


def admin_toggle_staff(request, user_id):
    if request.user.email != 'maheksavaliya3004@gmail.com' or request.user.username != 'MAHEK':
        return redirect('login')
    user = get_object_or_404(FitnessProfile, id=user_id)
    user.is_staff = not user.is_staff
    user.save()
    status = "granted staff" if user.is_staff else "revoked staff from"
    messages.success(request, f"Successfully {status} user '{user.username}'.")
    return redirect('admin_dashboard')


def admin_delete_meal_plan(request, plan_id):
    if request.user.email != 'maheksavaliya3004@gmail.com' or request.user.username != 'MAHEK':
        return redirect('login')
    plan = get_object_or_404(MealPlan, id=plan_id)
    plan.delete()
    messages.success(request, "Meal plan deleted.")
    return redirect('admin_dashboard')


def admin_delete_payment(request, payment_id):
    if request.user.email != 'maheksavaliya3004@gmail.com' or request.user.username != 'MAHEK':
        return redirect('login')
    from store.models import Payment
    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    messages.success(request, "Payment record deleted.")
    return redirect('admin_dashboard')
