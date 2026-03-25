"""
Decorators for restricting access based on membership status
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def membership_required(membership_type=None):
    """
    Decorator to restrict view access based on membership type.
    
    Usage:
        @membership_required()  # Requires any paid membership
        @membership_required('premium')  # Requires premium or higher
        @membership_required('elite')  # Requires elite membership
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, '🔐 Please login first to access this feature.')
                return redirect('login')
            
            user_membership = request.user.membership_type
            
            # If no specific membership required, just need to be authenticated
            if membership_type is None:
                if user_membership == 'free':
                    messages.info(request, '💳 Upgrade your membership to unlock premium features!')
                    return redirect('/#membership-plans')
                return view_func(request, *args, **kwargs)
            
            # Check for specific membership type
            membership_hierarchy = {'free': 0, 'premium': 1, 'elite': 2}
            user_level = membership_hierarchy.get(user_membership, 0)
            required_level = membership_hierarchy.get(membership_type, 1)
            
            if user_level < required_level:
                messages.warning(request, f'⚠️ This feature requires {membership_type.upper()} membership. Upgrade now!')
                return redirect('/#membership-plans')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator
