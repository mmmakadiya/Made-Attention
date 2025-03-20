from django.contrib import admin
from .models import Category, Subcategory, MeditationTechnique, User, Comment

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1

class MeditationTechniqueInline(admin.TabularInline):
    model = MeditationTechnique
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    inlines = [SubcategoryInline]

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    inlines = [MeditationTechniqueInline]

@admin.register(MeditationTechnique)
class MeditationTechniqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'difficulty_level', 'created_at')
    list_filter = ('subcategory', 'difficulty_level')
    search_fields = ('name', 'short_description', 'instructions')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'joined_date')
    search_fields = ('username', 'email')
    filter_horizontal = ('favorite_techniques',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'technique', 'created_at')
    list_filter = ('technique',)
    search_fields = ('content',)