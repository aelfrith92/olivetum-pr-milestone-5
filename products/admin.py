from django.contrib import admin
from .models import Product, Category, Review, Provider


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
        'provider',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewAdmin(admin.ModelAdmin):
    """Forms and actions in the admin area"""
    list_display = ('id', 'product', 'name', 'email', 'title', 'body',
                    'approved', 'single_rating')
    search_fields = ['title', 'body']
    list_filters = ('single_rating', 'approved')
    actions = ['approve_review', 'hide_review']

    def approve_review(self, request, queryset):
        """Show the function approve review in the admin overview"""
        queryset.update(approved=True)

    def hide_review(self, request, queryset):
        """Show the function hide review in the admin overview"""
        queryset.update(approved=False)


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('point_of_contact', 'business_name', 'risk_lev', 'city',
                    'location', 'ship_abroad', 'slr_rating')
    list_filter = ('city', 'ship_abroad', 'slr_rating')
    search_filter = ['point_of_contact', 'business_name', 'city']
    actions = ['set_high_risk']

    def set_high_risk(self, request, queryset):
        """Set risk level to high"""
        queryset.update(risk_lev=3)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Provider, ProviderAdmin)
