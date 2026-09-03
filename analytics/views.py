from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count

from orders.models import Order, OrderItem
from products.models import Product
from recommendations.models import UserInteraction
from wishlist.models import WishlistItem


@staff_member_required
def dashboard(request):

    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    total_revenue = (
        Order.objects
        .filter(status__in=["CONFIRMED", "SHIPPED", "DELIVERED"])
        .aggregate(total=Sum("total_amount"))["total"]
        or 0
    )

    pending_orders = Order.objects.filter(
        status="PENDING"
    ).count()

    delivered_orders = Order.objects.filter(
        status="DELIVERED"
    ).count()
        # Order Status Analytics
    order_status_data = []

    for status_code, status_name in Order.STATUS_CHOICES:
        count = Order.objects.filter(
            status=status_code
        ).count()

        order_status_data.append({
            "label": status_name,
            "count": count,
        })

    total_views = UserInteraction.objects.filter(
        interaction_type="VIEW"
    ).count()

    total_carts = UserInteraction.objects.filter(
        interaction_type="CART"
    ).count()

    total_purchases = UserInteraction.objects.filter(
        interaction_type="PURCHASE"
    ).count()

    total_wishlist = WishlistItem.objects.count()

    top_products = (
        OrderItem.objects
        .values("product__name")
        .annotate(
            total_sold=Sum("quantity")
        )
        .order_by("-total_sold")[:5]
    )

    top_viewed_products = (
        UserInteraction.objects
        .filter(interaction_type="VIEW")
        .values("product__name")
        .annotate(
            total_views=Count("id")
        )
        .order_by("-total_views")[:5]
    )
        # Chart data

    top_products_chart = [
        {
            "label": product["product__name"],
            "value": product["total_sold"],
        }
        for product in top_products
    ]

    most_viewed_chart = [
        {
            "label": product["product__name"],
            "value": product["total_views"],
        }
        for product in top_viewed_products
    ]

    order_status_chart = [
        {
            "label": item["label"],
            "value": item["count"],
        }
        for item in order_status_data
    ]

    context = {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "order_status_data": order_status_data,
        "top_products_chart": top_products_chart,
        "most_viewed_chart": most_viewed_chart,
        "order_status_chart": order_status_chart,
        "total_views": total_views,
        "total_carts": total_carts,
        "total_purchases": total_purchases,
        "total_wishlist": total_wishlist,
        "top_products": top_products,
        "top_viewed_products": top_viewed_products,
    }

    return render(
        request,
        "analytics/dashboard.html",
        context
    )
