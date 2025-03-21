from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'last_login')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'purpose', 'created_at', 'is_verified')
    search_fields = ('user__email', 'otp')
    list_filter = ('purpose', 'is_verified', 'created_at')
    readonly_fields = ('created_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP, OTPAdmin)