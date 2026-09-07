from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("products.urls")
    ),

    path(
        "cart/",
        include("orders.urls")
    ),

    path(
        "accounts/",
        include("accounts.urls")
    ),
        path(
        "wishlist/",
        include("wishlist.urls")
    ),
    path("analytics/", include("analytics.urls")), 
]
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]