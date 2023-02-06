from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail.as_view(),
         name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product,
         name='delete_product'),
    path('delreview/<int:review_id>/', views.delete_review,
         name='delete_review'),
    path('hidereview/<int:review_id>/', views.hide_review,
         name='hide_review'),
    path('unhidereview/<int:review_id>/', views.unhide_review,
         name='unhide_review'),
]
