from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Category, Subcategory, MeditationTechnique, User, Comment

def front(request):
    return render(request, 'front.html')

def home(request):
    
    """Homepage view"""
    categories = Category.objects.all()[:6]  # Get first 6 categories for showcase
    techniques = MeditationTechnique.objects.all().order_by('-created_at')[:6]  # Recent techniques
    
    context = {
        'categories': categories,
        'techniques': techniques,
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