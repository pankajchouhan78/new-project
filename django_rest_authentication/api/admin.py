from django.contrib import admin
from .models import Book
# Register your models here.

# @admin.register('Book')
# class BookAdmin(admin.ModelAdmin):
#     class Meta:
#         list_display = ['title','description']


admin.site.register(Book)