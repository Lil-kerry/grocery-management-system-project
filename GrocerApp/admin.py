from django.contrib import admin
from .models import Category, Product, Review, Blog, Subscriber

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')
    search_fields = ('name', 'price')

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Blog)
admin.site.register(Subscriber,SubscriberAdmin)