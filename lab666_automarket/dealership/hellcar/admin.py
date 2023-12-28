from django.contrib import admin
from .models import Car, Brand, Category, Review

class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'category', 'price')  
    list_filter = ('brand', 'category')  
    search_fields = ('model', 'description')  

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'text')  
    list_filter = ('car', 'user', 'rating')  
    search_fields = ('text', 'car__model')  



admin.site.register(Car, CarAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)