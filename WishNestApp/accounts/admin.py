from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from WishNestApp.accounts.forms import UserCreateForm, UserEditForm

UserModel = get_user_model()

@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    model = UserModel
    add_form = UserCreateForm
    form = UserEditForm

    # list_display = ('pk', 'email', 'is_staff', 'is_superuser')
    # search_fields = ('email',)
    # ordering = ('pk',)
    #
    # fieldsets = ((None, {'fields': ('email', 'password')}), ('Personal info', {'fields': ()}),
    #              ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    #              ('Important dates', {'fields': ('last_login',)}),)
    #
    # add_fieldsets = ((None, {"classes": ("wide",),
    #                          "fields": ("email", "password1", "password2"), }))
