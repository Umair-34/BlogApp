from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin, SummernoteModelAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name',
            'profile_picture_preview', 'profile_picture',
            'description',
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'updated_at')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('updated_at', 'profile_picture_preview')

    def profile_picture_preview(self, obj):
        return obj.profile_picture_preview

    profile_picture_preview.short_description = 'Thumbnail Preview'
    profile_picture_preview.allow_tags = True

    summernote_fields = ('description',)
