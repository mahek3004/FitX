from django.shortcuts import render, redirect
from .models import MealPlan
from django.contrib.auth.decorators import login_required

def diet_home(request):
    if request.user.is_authenticated:
        meal_plans = MealPlan.objects.filter(user=request.user)
    else:
        meal_plans = []
        
    return render(request, 'diet/diet.html', {'meal_plans': meal_plans})

@login_required
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
