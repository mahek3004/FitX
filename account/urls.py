from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('progress/log/', views.log_progress, name='log_progress'),

    # Frontend Admin Dashboard (staff only)
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/delete-user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-panel/toggle-staff/<int:user_id>/', views.admin_toggle_staff, name='admin_toggle_staff'),
    path('admin-panel/delete-meal-plan/<int:plan_id>/', views.admin_delete_meal_plan, name='admin_delete_meal_plan'),
    path('admin-panel/delete-payment/<int:payment_id>/', views.admin_delete_payment, name='admin_delete_payment'),
]
