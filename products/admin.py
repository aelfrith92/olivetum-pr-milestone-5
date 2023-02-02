from django.contrib import admin
from .models import Product, Category, Review, Comment, Provider

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewAdmin(admin.ModelAdmin):
    """Forms and actions in the admin area"""
    list_display = ('product', 'name', 'email', 'title', 'body',
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
    
    
class CommentAdmin(admin.ModelAdmin):
    '''This class defines forms and related actions/tools in the admin area
    Comment management'''
    list_display = ('name', 'body', 'product', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comments', 'hide_comments']

    def approve_comments(self, request, queryset):
        '''Adds the function Approve Comment to possible actions in
        the admin area'''
        queryset.update(approved=True)
    
    def hide_comments(self, request, queryset):
        '''Adds the function Hide Comment to possible actions in
        the admin area'''
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
admin.site.register(Comment, CommentAdmin)
admin.site.register(Provider, ProviderAdmin)
