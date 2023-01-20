from django.contrib import admin
from . models import Product, Category, Tag, Comment

admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'available')
    list_filter = ('available', )
    search_fields = ('name', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

admin.site.register(Comment)

# Register your models here.
