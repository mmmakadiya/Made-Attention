from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm, 
    OTPLoginForm, 
    VerifyOTPForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm
)
from .models import CustomUser, OTP


def register_view(request):
    if request.user.is_authenticated:
        return redirect('meditation:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Generate verification OTP
            otp_obj = OTP.generate_otp(user, purpose='verification')
            # Send OTP to user's email
            send_otp_email(user.email, otp_obj.otp, 'Account Verification')
            
            login(request, user)
            messages.success(request, "Registration successful! Please verify your email.")
            return redirect('meditation:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def front_page_view(request):
    if request.user.is_authenticated:
        return redirect('meditation:home')  # Redirect logged-in users to home
    return render(request, 'front.html')  # Show front page only to non-logged-in users


def login_view(request):
    if request.user.is_authenticated:
        return redirect('meditation:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in successfully!")
                return redirect('meditation:home')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {
        'form': form,
        'otp_form': OTPLoginForm()
    })


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('login')


def otp_login_request(request):
    if request.method == 'POST':
        form = OTPLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                # Generate OTP for login
                otp_obj = OTP.generate_otp(user, purpose='login')
                # Send OTP email
                send_otp_email(user.email, otp_obj.otp, 'Login')
                
                # Store email in session for verification step
                request.session['otp_email'] = email
                request.session['otp_purpose'] = 'login'
                
                messages.success(request, "OTP has been sent to your email!")
                return redirect('verify_otp')
            except CustomUser.DoesNotExist:
                messages.error(request, "No account found with this email address.")
                return redirect('login')
    
    return redirect('login')


def verify_otp_view(request):
    email = request.session.get('otp_email')
    purpose = request.session.get('otp_purpose')
    
    if not email or not purpose:
        messages.error(request, "Invalid session. Please try again.")
        return redirect('login')
    
    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data.get('otp')
            try:
                user = CustomUser.objects.get(email=email)
                # Get the latest unused OTP for this user and purpose
                otp_obj = OTP.objects.filter(
                    user=user,
                    purpose=purpose,
                    is_verified=False,
                    expires_at__gt=timezone.now()
                ).latest('created_at')
                
                if otp_obj.otp == otp_entered:
                    # Mark OTP as verified
                    otp_obj.is_verified = True
                    otp_obj.save()
                    
                    # Handle based on purpose
                    if purpose == 'login':
                        login(request, user)
                        messages.success(request, "Login successful!")
                        return redirect('home')
                    elif purpose == 'password_reset':
                        request.session['reset_user_id'] = user.id
                        return redirect('reset_password')
                    elif purpose == 'verification':
                        user.is_active = True
                        user.save()
                        messages.success(request, "Email verified successfully!")
                        return redirect('home')
                else:
                    messages.error(request, "Invalid OTP. Please try again.")
            except (CustomUser.DoesNotExist, OTP.DoesNotExist):
                messages.error(request, "Invalid OTP or OTP expired. Please try again.")
        else:
            messages.error(request, "Please enter a valid 6-digit OTP.")
    
    form = VerifyOTPForm()
    return render(request, 'users/verify_otp.html', {
        'form': form,
        'email': email,
        'purpose': purpose
    })

def otp_login_view(request):
    email = request.POST.get('email')
    try:
        user = CustomUser.objects.get(email=email)
        otp = OTP.generate_otp(user, 'login')
        send_otp_email(email, otp.otp, 'Login')
        request.session['login_email'] = email
        return JsonResponse({'success': True, 'message': 'OTP sent to your email'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'No account found with that email'})



def forgot_password_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                # Generate OTP for password reset
                otp_obj = OTP.generate_otp(user, purpose='password_reset')
                # Send OTP email
                send_otp_email(user.email, otp_obj.otp, 'Password Reset')
                
                # Store email in session for verification step
                request.session['otp_email'] = email
                request.session['otp_purpose'] = 'password_reset'
                
                messages.success(request, "Password reset OTP has been sent to your email!")
                return redirect('verify_otp')
            except CustomUser.DoesNotExist:
                # For security reasons, don't reveal that the email doesn't exist
                messages.success(request, "If an account exists with this email, a password reset OTP has been sent.")
                return redirect('login')
    else:
        form = CustomPasswordResetForm()
    
    return render(request, 'users/forgot_password.html', {'form': form})


def reset_password_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Invalid session. Please try again.")
        return redirect('forgot_password')
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found. Please try again.")
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            # Clear session data
            del request.session['reset_user_id']
            del request.session['otp_email']
            del request.session['otp_purpose']
            
            messages.success(request, "Your password has been reset successfully! You can now login with your new password.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomSetPasswordForm(user)
    
    return render(request, 'users/reset_password.html', {'form': form})


def verify_otp_ajax(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        otp_entered = request.POST.get('otp')
        email = request.session.get('otp_email')
        purpose = request.session.get('otp_purpose')
        
        if not email or not purpose or not otp_entered:
            return JsonResponse({'valid': False, 'message': 'Invalid request'})
        
        try:
            user = CustomUser.objects.get(email=email)
            otp_obj = OTP.objects.filter(
                user=user,
                purpose=purpose,
                is_verified=False,
                expires_at__gt=timezone.now()
            ).latest('created_at')
            
            if otp_obj.otp == otp_entered:
                return JsonResponse({'valid': True})
            else:
                return JsonResponse({'valid': False, 'message': 'Invalid OTP'})
        except (CustomUser.DoesNotExist, OTP.DoesNotExist):
            return JsonResponse({'valid': False, 'message': 'Invalid OTP or OTP expired'})
    
    return JsonResponse({'valid': False, 'message': 'Invalid request'})


# Helper function to send OTP emails
def send_otp_email(email, otp, purpose):
    subject_map = {
        'Login': 'Login OTP for Meditation App',
        'Password Reset': 'Password Reset OTP for Meditation App',
        'Account Verification': 'Verify Your Meditation App Account'
    }
    
    message_map = {
        'Login': f'Your OTP for logging into the Meditation App is: {otp}. This OTP will expire in 10 minutes.',
        'Password Reset': f'Your OTP for resetting your Meditation App password is: {otp}. This OTP will expire in 10 minutes.',
        'Account Verification': f'Your OTP for verifying your Meditation App account is: {otp}. This OTP will expire in 10 minutes.'
    }
    
    subject = subject_map.get(purpose, f'{purpose} OTP for Meditation App')
    message = message_map.get(purpose, f'Your OTP for {purpose.lower()} is: {otp}. This OTP will expire in 10 minutes.')
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False