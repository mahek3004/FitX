from django.shortcuts import render, redirect
from .models import MealPlan
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

@login_required
def diet_home(request):
    meal_plans = MealPlan.objects.filter(user=request.user).order_by('id')
    
    # If free user and no custom plans - provide sample 7 days
    if not meal_plans.exists() and request.user.membership_type == 'free':
        sample_meals = []
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for day in days:
            sample_meals.append({
                'day_of_week': day.title(),
                'meal_name': 'Free Trial Plan - Day ' + day.title(),
                'breakfast': 'Oatmeal with Almonds and Fruits',
                'lunch': 'Grilled Chicken or Paneer with Veggie Salad',
                'dinner': 'Lentil Soup / Dal with Brown Rice',
                'snacks': 'Roasted Gram or Walnuts',
                'calories': 1800,
                'protein': 90,
                'carbs': 150,
                'fats': 45
            })
        return render(request, 'diet/diet.html', {
            'meal_plans': sample_meals, 
            'is_trial': True
        })
        
    return render(request, 'diet/diet.html', {'meal_plans': meal_plans})

from core.decorators import membership_required

@membership_required()
def save_diet_plan(request):
    if request.method == 'POST':
        calories = int(float(request.POST.get('calories', 2000)))
        
        # Replace existing ones
        MealPlan.objects.filter(user=request.user).delete()
        
        breakfast = request.POST.get('breakfast', 'Oats')
        lunch = request.POST.get('lunch', 'Rice')
        dinner = request.POST.get('dinner', 'Salad')
        snacks = request.POST.get('snacks', 'Nuts')
        
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for day in days:
            MealPlan.objects.create(
                user=request.user,
                day_of_week=day,
                meal_name=f"{breakfast[:30]} | {lunch[:30]} | {dinner[:30]}",
                breakfast=breakfast,
                lunch=lunch,
                dinner=dinner,
                snacks=snacks,
                calories=calories,
                protein=round(calories * 0.3 / 4),
                carbs=round(calories * 0.4 / 4),
                fats=round(calories * 0.3 / 9)
            )
            
        return redirect('dashboard')
    return redirect('diet')
