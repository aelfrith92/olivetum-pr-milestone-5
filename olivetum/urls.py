from django.contrib import admin
from products import views
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls.static import static
from .views import handler404, handler500, handler403, handler400

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
    path('contactform/', views.contactform, name='contactform'),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'olivetum.views.handler404'
handler500 = 'olivetum.views.handler500'
handler403 = 'olivetum.views.handler403'
handler400 = 'olivetum.views.handler400'
