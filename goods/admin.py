from django.contrib import admin

from goods.models import Categories, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'quantity', 'price', 'discount')
    list_editable = ('discount', "price")
    search_fields = ['name', 'description']
    list_filter = ('discount', 'quantity', 'category')
    fields = [
        'name',
        'category',
        'slug',
        'description',
        'image',
        ('price', 'discount'),
        'quantity'
    ]

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name',)