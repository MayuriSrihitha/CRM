from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Record, UserProfile

# Custom admin site configuration
admin.site.site_header = 'CRM Administration'
admin.site.site_title = 'CRM Admin Portal'
admin.site.index_title = 'Welcome to CRM Admin Portal'

# Custom Record Admin
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'city', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'city', 'state', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at', 'last_updated')
    ordering = ('-created_at',)
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Personal Information', {
            'fields': (('first_name', 'last_name'), 'email', 'phone'),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Address Details', {
            'fields': ('address', ('city', 'state', 'zipcode')),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Record Status', {
            'fields': (('status', 'assigned_to'), ('created_at', 'last_updated')),
            'classes': ('wide', 'extrapretty'),
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

    class Media:
        css = {
            'all': ['admin/css/custom_admin.css']
        }

# Custom UserProfile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'date_joined')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'user__email')
    ordering = ('-user__date_joined',)

    def username(self, obj):
        return obj.user.username
    
    def email(self, obj):
        return obj.user.email
    
    def date_joined(self, obj):
        return obj.user.date_joined
    
    date_joined.admin_order_field = 'user__date_joined'
