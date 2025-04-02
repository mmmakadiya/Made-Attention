from django.urls import path
from . import views

app_name = 'meditation'

urlpatterns = [
    path('', views.front, name='front'),
    path('home/', views.home, name='home'),
        path('categories/', views.category_list, name='categories'),  # Ensure this exists
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('subcategories/<int:subcategory_id>/', views.subcategory_detail, name='subcategory_detail'),
    path('techniques/<int:technique_id>/', views.technique_detail, name='technique_detail'),
    path('library/', views.library, name='library'),
    path('community/', views.community, name='community'),
    path('settings/', views.settings_page, name='settings'),
    
]