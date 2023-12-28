from django.contrib import admin
from .models import Car, Brand, Category

class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'category', 'price')  # Поля для отображения в списке
    list_filter = ('brand', 'category')  # Фильтры
    search_fields = ('model', 'description')  # Поля поиска

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

admin.site.register(Car, CarAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
