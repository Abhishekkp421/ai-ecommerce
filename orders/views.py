from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import CartItem
from django.db import transaction
from recommendations.models import UserInteraction

from django.contrib.auth.decorators import login_required

from .models import Order, OrderItem


def get_session_key(request):
    if not request.session.session_key:
        request.session.create()

    return request.session.session_key


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(
            request,
            f"{product.name} is currently out of stock."
        )
        return redirect("products")

    session_key = get_session_key(request)

    cart_item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        product=product
    )

    if not created:

        if cart_item.quantity >= product.stock:
            messages.error(
                request,
                f"Only {product.stock} items of {product.name} are available."
            )
            return redirect("cart")

        cart_item.quantity += 1
        cart_item.save()

    UserInteraction.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=session_key,
        product=product,
        interaction_type="CART"
    )

    return redirect("cart")


def cart(request):
    session_key = get_session_key(request)

    cart_items = CartItem.objects.filter(
        session_key=session_key
    )

    total = sum(item.total_price() for item in cart_items)

    return render(
        request,
        "orders/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


def remove_from_cart(request, item_id):
    session_key = get_session_key(request)

    item = get_object_or_404(
        CartItem,
        id=item_id,
        session_key=session_key
    )

    item.delete()

    return redirect("cart") 
def increase_quantity(request, item_id):
    session_key = get_session_key(request)

    item = get_object_or_404(
        CartItem,
        id=item_id,
        session_key=session_key
    )

    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()

    return redirect("cart")


def decrease_quantity(request, item_id):
    session_key = get_session_key(request)

    item = get_object_or_404(
        CartItem,
        id=item_id,
        session_key=session_key
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect("cart")
from django.contrib.auth.decorators import login_required


@login_required
def checkout(request):
    session_key = get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items.exists():
        return redirect("cart")

    # Check stock before checkout
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f"{item.product.name} has only "
                f"{item.product.stock} items available."
            )
            return redirect("cart")

    total = sum(
        item.total_price()
        for item in cart_items
    )

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        pincode = request.POST.get("pincode", "").strip()

        # Basic input validation
        if not full_name or not email or not address or not city or not pincode:
            messages.error(
                request,
                "All delivery fields are required."
            )
            return redirect("checkout")

        if len(full_name) < 3:
            messages.error(
                request,
                "Please enter a valid full name."
            )
            return redirect("checkout")

        try:
            validate_email(email)
        except ValidationError:
            messages.error(
                request,
                "Please enter a valid email address."
            )
            return redirect("checkout")

        if len(address) < 10:
            messages.error(
                request,
                "Please enter a valid address."
            )
            return redirect("checkout")

        if not pincode.isdigit() or len(pincode) != 6:
            messages.error(
                request,
                "Pincode must be exactly 6 digits."
            )
            return redirect("checkout")

        # Complete order process inside one transaction
        with transaction.atomic():

            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                email=email,
                address=address,
                city=city,
                pincode=pincode,
                total_amount=total,
            )

            for item in cart_items:

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

                UserInteraction.objects.create(
                    user=request.user,
                    session_key=session_key,
                    product=item.product,
                    interaction_type="PURCHASE"
                )

                item.product.stock -= item.quantity
                item.product.save()

            cart_items.delete()

        return redirect(
            "order_success",
            order_id=order.id
        )

    return render(
        request,
        "orders/checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )
@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order,
        }
    ) 
@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        "items__product"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders
        }
    )