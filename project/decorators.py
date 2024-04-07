from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


# DECORATOR TO REDIRECT USERS IF THEY ARE LOGGED IN AND WANT TO LOGGED IN
def redirect_if_logged_in(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged In!")
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapper


# DECORATOR TO REDIRECT USERS IF THEY ARE LOGGED OUT AND WANT TO LOGOUT
def redirect_if_logged_out(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request,
                "You are already logged Out!, please login if you have an account!",
            )
            return redirect("login2")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


# DECORATOR TO REDIRECT USERS IF THEY WANT TO ACCESS A PAGE AND THEY ARE NOT LOGGED IN
def login_required_with_message(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary and adds a message.
    """

    def check_user_logged_in(user):
        return user.is_authenticated

    actual_decorator = user_passes_test(
        check_user_logged_in,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, "You must be logged in to access this page!")
            return actual_decorator(view_func)(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)
    return decorator
