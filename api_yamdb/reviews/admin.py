from django.contrib import admin
from .models import User, Genre, Category, Title, Genre_Title


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'bio',
        'created_at',
        'modified_at',
    )
    search_fields = ('username', 'email')
    list_filter = ('created_at',)
    empty_value_display = '-empty-'


admin.site.register(User, UserAdmin)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Genre_Title)
