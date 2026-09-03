from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.urls import reverse

from .models import EmailVerification


def register(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        # Required fields
        if not username or not email or not password:
            messages.error(
                request,
                "All fields are required."
            )
            return redirect("register")

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(
                request,
                "Please enter a valid email address."
            )
            return redirect("register")

        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Username already exists."
            )
            return redirect("register")

        # Check email
        if User.objects.filter(email__iexact=email).exists():
            messages.error(
                request,
                "An account with this email already exists."
            )
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # User cannot login until email is verified
        user.is_active = False
        user.save()

        # Create verification record
        verification = EmailVerification.objects.create(
            user=user
        )

        # Create verification URL
        verification_url = request.build_absolute_uri(
            reverse(
                "verify_email",
                kwargs={"token": verification.token}
            )
        )

        # Send verification email
        send_mail(
            subject="Verify your AI Shop email",
            message=(
                f"Hello {username},\n\n"
                f"Thank you for registering on AI Shop.\n\n"
                f"Please verify your email by clicking the link below:\n\n"
                f"{verification_url}\n\n"
                f"If you did not create this account, you can ignore this email."
            ),
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(
            request,
            "Registration successful! Please check your email to verify your account."
        )

        return redirect("login")

    return render(
        request,
        "accounts/register.html"
    )


def verify_email(request, token):

    verification = get_object_or_404(
        EmailVerification,
        token=token
    )

    if verification.is_verified:
        messages.info(
            request,
            "Your email is already verified."
        )
        return redirect("login")

    verification.is_verified = True
    verification.save()

    user = verification.user
    user.is_active = True
    user.save()

    messages.success(
        request,
        "Email verified successfully! You can now login."
    )

    return redirect("login")


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/")

        # Check if account exists but email is not verified
        try:
            existing_user = User.objects.get(
                username=username
            )

            if not existing_user.is_active:
                messages.error(
                    request,
                    "Please verify your email before logging in."
                )
            else:
                messages.error(
                    request,
                    "Invalid username or password."
                )

        except User.DoesNotExist:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "accounts/login.html"
    )


def user_logout(request):

    logout(request)

    return redirect("/")