from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Category, Subcategory, MeditationTechnique, User, Comment
from datetime import datetime
from django.utils import timezone

def front(request):
    return render(request, 'front.html')

def home(request):
    # Get current time
    current_time = timezone.now()
    current_hour = current_time.hour
    
    # Determine time of day
    if 5 <= current_hour < 12:
        time_of_day = "Morning"
        time_tag = "morning"
    elif 12 <= current_hour < 17:
        time_of_day = "Noon"
        time_tag = "noon"
    elif 17 <= current_hour < 21:
        time_of_day = "Evening"
        time_tag = "evening"
    else:
        time_of_day = "Night"
        time_tag = "night"
    
    # Get categories and all techniques
    categories = Category.objects.all()[:6]  # Limit to 6 categories
    all_techniques = MeditationTechnique.objects.all()
    
    # Get time-based techniques (modify as per your model's structure)
    time_based_techniques = all_techniques.filter(duration__gte=10)[:3]
    
    context = {
        'categories': categories,
        'time_of_day': time_of_day,
        'current_time': current_time,
        'time_based_techniques': time_based_techniques,
        'all_techniques': all_techniques,  # Add all techniques to context
    }
    
    return render(request, 'home.html', context)

def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    return render(request, 'categories/list.html', {'categories': categories})

def category_detail(request, category_id):
    """Show details of a specific category and its subcategories"""
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    
    context = {
        'category': category,
        'subcategories': subcategories,
    }
    return render(request, 'categories/detail.html', context)

def subcategory_detail(request, subcategory_id):
    """Show details of a specific subcategory and its techniques"""
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    techniques = subcategory.techniques.all()
    
    context = {
        'subcategory': subcategory,
        'techniques': techniques,
    }
    return render(request, 'categories/subcategory_detail.html', context)

def technique_detail(request, technique_id):
    """Show detailed information about a specific meditation technique"""
    technique = get_object_or_404(MeditationTechnique, id=technique_id)
    comments = technique.comments.all().order_by('-created_at')
    
    context = {
        'technique': technique,
        'comments': comments,
    }
    return render(request, 'categories/technique_detail.html', context)

def library(request):
    """View for the library page"""
    techniques = MeditationTechnique.objects.all()
    
    # Filtering options
    category_filter = request.GET.get('category')
    difficulty_filter = request.GET.get('difficulty')
    
    if category_filter:
        techniques = techniques.filter(subcategory__category__id=category_filter)
    
    if difficulty_filter:
        techniques = techniques.filter(difficulty_level=difficulty_filter)
    
    context = {
        'techniques': techniques,
        'categories': Category.objects.all(),
    }
    return render(request, 'library.html', context)

def community(request):
    """View for the community page"""
    recent_comments = Comment.objects.all().order_by('-created_at')[:20]
    users = User.objects.all()[:10]  # Show some users
    
    context = {
        'comments': recent_comments,
        'users': users,
    }
    return render(request, 'community.html', context)

def settings_page(request):
    """View for the settings page"""
    return render(request, 'settings.html')