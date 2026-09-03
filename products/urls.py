from django.urls import path
from .views import home, product_list, product_detail, category_list

urlpatterns = [

    path(
        "",
        home,
        name="home"
    ),

    path(
        "products/",
        product_list,
        name="products"
    ),

    path(
        "product/<slug:slug>/",
        product_detail,
        name="product_detail"
    ),
    path(
    "categories/",
    category_list,
    name="categories"
 ),
]