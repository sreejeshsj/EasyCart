from django.contrib import admin
from . models import Accounts
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=('email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links=('email','first_name','username')
    filter_horizontal=()
    list_filter=()
    fieldsets=()
    readonly_fields=['last_login','date_joined']
    ordering=('-date_joined',)
admin.site.register(Accounts,AccountAdmin)
