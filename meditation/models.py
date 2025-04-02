from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_tags = models.JSONField(default=list)  # ✅ Ensure this exists

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Technique(models.Model):
    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    
    TIME_TAG_CHOICES = (
        ('morning', 'Morning'),
        ('noon', 'Noon'),
        ('evening', 'Evening'),
        ('night', 'Night'),
    )
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='techniques')
    short_description = models.TextField()
    detailed_description = models.TextField()
    duration_minutes = models.PositiveIntegerField(default=10)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    image = models.ImageField(upload_to='techniques/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_tags = models.JSONField(default=list)  # ✅ Ensure this exists

    
    # Add this field for time-based recommendations
    # You can use a ManyToManyField if you want to allow multiple time tags
    time_tags = models.CharField(max_length=50, choices=TIME_TAG_CHOICES, blank=True)
    
    # Alternative: Use a ManyToManyField if techniques can belong to multiple times of day
    # time_tags = models.ManyToManyField('TimeTag', blank=True, related_name='techniques')
    
    def __str__(self):
        return self.name

# class Category(models.Model):
#     """Main category model (e.g., Breathing-based meditation, Silent meditation)"""
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='categories/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name_plural = "Categories"
    
#     def __str__(self):
#         return self.name

class Subcategory(models.Model):
    """Subcategory model (e.g., Vipassana, Nadbrahma under Breathing-based)"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='subcategories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Subcategories"
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"

class MeditationTechnique(models.Model):
    """Individual meditation technique (e.g., specific Vipassana technique)"""
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='techniques')
    name = models.CharField(max_length=100)
    short_description = models.TextField()
    benefits = models.TextField()
    instructions = models.TextField()
    duration = models.CharField(max_length=50, help_text="Recommended duration")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])
    image = models.ImageField(upload_to='techniques/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class User(models.Model):
    """User profile model for community features"""
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    favorite_techniques = models.ManyToManyField(MeditationTechnique, related_name='favorited_by', blank=True)
    
    def __str__(self):
        return self.username

class Comment(models.Model):
    """Comments on meditation techniques for community interaction"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    technique = models.ForeignKey(MeditationTechnique, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.technique.name}"
    
class Technique(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name