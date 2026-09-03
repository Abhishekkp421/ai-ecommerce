from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When

from .models import Product, Category
from recommendations.models import UserInteraction
from recommendations.recommender import get_similar_products
from recommendations.recommender import smart_search
from wishlist.models import WishlistItem


def home(request):
    products = Product.objects.all()[:4]

    return render(
        request,
        "products/home.html",
        {
            "products": products,
        }
    )


def product_list(request):

    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    sort = request.GET.get("sort", "")

    products = Product.objects.all()

    # Search
    if query:
        smart_products = smart_search(query)

        if smart_products:
            product_ids = [
                product.id
                for product in smart_products
            ]

            products = Product.objects.filter(
                id__in=product_ids
            ).order_by(
                Case(
                    *[
                        When(
                            id=product_id,
                            then=index
                        )
                        for index, product_id
                        in enumerate(product_ids)
                    ]
                )
            )
        else:
            products = products.none()

    # Category
    if category:
        products = products.filter(
            category__name__iexact=category
        )

    # Minimum price
    if min_price:
        products = products.filter(
            price__gte=min_price
        )

    # Maximum price
    if max_price:
        products = products.filter(
            price__lte=max_price
        )

    # Sorting
    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "newest":
        products = products.order_by("-created_at")

    elif sort == "oldest":
        products = products.order_by("created_at")

    # Wishlist products
    wishlist_product_ids = set()

    if request.user.is_authenticated:
        wishlist_product_ids = set(
            WishlistItem.objects.filter(
                user=request.user
            ).values_list(
                "product_id",
                flat=True
            )
        )

    categories = Category.objects.all()

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "query": query,
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "sort": sort,
            "categories": categories,
            "wishlist_product_ids": wishlist_product_ids,
        }
    )


def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug
    )

    if not request.session.session_key:
        request.session.create()

    UserInteraction.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key,
        product=product,
        interaction_type="VIEW"
    )

    similar_products = get_similar_products(
        product,
        user=request.user,
        session_key=request.session.session_key,
        limit=4
    )

    recommendation_reason = (
        "Similar to the product you're viewing."
    )

    if request.user.is_authenticated:
        has_interactions = UserInteraction.objects.filter(
            user=request.user
        ).exists()

        if has_interactions:
            recommendation_reason = (
                "Recommended based on your recent activity."
            )

    is_wishlisted = False

    if request.user.is_authenticated:
        is_wishlisted = WishlistItem.objects.filter(
            user=request.user,
            product=product
        ).exists()

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "similar_products": similar_products,
            "recommendation_reason": recommendation_reason,
            "is_wishlisted": is_wishlisted,
        }
    )


def category_list(request):

    categories = Product.objects.values(
        "category__id",
        "category__name"
    ).distinct()

    return render(
        request,
        "products/categories.html",
        {
            "categories": categories,
        }
    )