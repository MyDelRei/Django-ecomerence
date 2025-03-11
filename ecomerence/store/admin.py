from django.contrib import admin

# Register your models here.

from .models import Category, Product

from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

