from django.contrib import admin
from django.urls import path, include

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