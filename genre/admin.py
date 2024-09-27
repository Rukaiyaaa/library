from django.contrib import admin
from . import models

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('book_category', )}
    list_display = ['book_category', 'slug']

admin.site.register(models.BookCategory, BookAdmin)