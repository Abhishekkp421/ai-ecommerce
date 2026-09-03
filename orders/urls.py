from django.urls import path

from .views import (
    add_to_cart,
    cart,
    remove_from_cart,
    increase_quantity,
    decrease_quantity,
    checkout,
    order_success,
    my_orders,
)


urlpatterns = [

    path(
        "add/<int:product_id>/",
        add_to_cart,
        name="add_to_cart"
    ),

    path(
        "",
        cart,
        name="cart"
    ),

    path(
        "remove/<int:item_id>/",
        remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "increase/<int:item_id>/",
        increase_quantity,
        name="increase_quantity"
    ),

    path(
        "decrease/<int:item_id>/",
        decrease_quantity,
        name="decrease_quantity"
    ),

    path(
        "checkout/",
        checkout,
        name="checkout"
    ),

    path(
        "success/<int:order_id>/",
        order_success,
        name="order_success"
    ),
    path(
    "my-orders/",
    my_orders,
    name="my_orders"
),
] 
