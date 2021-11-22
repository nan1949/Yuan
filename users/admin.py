from django.contrib import admin
from .models import User


@admin.register(User)
class BookModel(admin.ModelAdmin):

    list_display = ('pk','name',  'email', )
    search_fields = ('name', 'email', )
    readonly_fields = ('pk', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()