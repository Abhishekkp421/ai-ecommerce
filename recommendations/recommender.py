import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from products.models import Product
from recommendations.models import UserInteraction


def get_similar_products(product, user=None, session_key=None, limit=4):

    products = list(
        Product.objects
        .select_related("category")
        .filter(stock__gt=0)
    )

    if len(products) < 2:
        return []

    # -------------------------------------------------
    # 1. Create product text
    # -------------------------------------------------

    data = []

    for item in products:

        combined_text = (
            f"{item.name} "
            f"{item.category.name} "
            f"{item.description}"
        )

        data.append({
            "id": item.id,
            "text": combined_text
        })

    df = pd.DataFrame(data)

    # -------------------------------------------------
    # 2. TF-IDF
    # -------------------------------------------------

    tfidf = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = tfidf.fit_transform(
        df["text"]
    )

    # -------------------------------------------------
    # 3. Product-to-product similarity
    # -------------------------------------------------

    similarity_matrix = cosine_similarity(
        tfidf_matrix
    )

    try:

        product_index = df.index[
            df["id"] == product.id
        ][0]

    except IndexError:

        return []

    content_scores = similarity_matrix[
        product_index
    ]

    # -------------------------------------------------
    # 4. Get user interactions
    # -------------------------------------------------

    interactions = UserInteraction.objects.none()

    if user is not None and user.is_authenticated:

        interactions = UserInteraction.objects.filter(
            user=user
        )

    elif session_key:

        interactions = UserInteraction.objects.filter(
            session_key=session_key
        ) 

        # -------------------------------------------------
    # 5. Interaction weights
    # -------------------------------------------------

    interaction_weights = {
        "VIEW": 1,
        "CART": 3,
        "PURCHASE": 5,
    }

    
    # -------------------------------------------------
    # 6. Create user preference profile
    # -------------------------------------------------

    user_profile = None

    if interactions.exists():

        interaction_weights = {
            "VIEW": 1,
            "CART": 3,
            "PURCHASE": 5,
        }

        weighted_vectors = []
        total_weight = 0

        for interaction in interactions:

            try:

                interaction_index = df.index[
                    df["id"] == interaction.product.id
                ][0]

            except IndexError:

                continue

            weight = interaction_weights.get(
                interaction.interaction_type,
                1
            )

            weighted_vectors.append(
                tfidf_matrix[interaction_index] * weight
            )

            total_weight += weight

        if weighted_vectors and total_weight > 0:

            user_profile = (
                sum(weighted_vectors)
                / total_weight
            )

    # -------------------------------------------------
    # 7. Calculate final recommendation score
    # -------------------------------------------------

    recommendation_scores = []

    for index, item_id in enumerate(df["id"]):

        # Never recommend the current product
        if int(item_id) == product.id:
            continue

        content_score = float(
            content_scores[index]
        )

        behavior_score = 0

        # If user has history
        if user_profile is not None:

            behavior_score = float(
                cosine_similarity(
                    tfidf_matrix[index],
                    user_profile
                )[0][0]
            )

            # Hybrid score
            final_score = (
                0.3 * content_score
                +
                0.7 * behavior_score
            )

        else:

            # New user → content based
            final_score = content_score

        recommendation_scores.append(
            (
                int(item_id),
                final_score
            )
        )

    # -------------------------------------------------
    # 8. Sort recommendations
    # -------------------------------------------------

    recommendation_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    recommended_ids = [
        item_id
        for item_id, score
        in recommendation_scores[:limit]
    ]

    # -------------------------------------------------
    # 9. Get products
    # -------------------------------------------------

    recommended_products = Product.objects.filter(
        id__in=recommended_ids
    )

    product_map = {
        item.id: item
        for item in recommended_products
    }

    return [
        product_map[item_id]
        for item_id in recommended_ids
        if item_id in product_map
    ] 
def smart_search(query, limit=20):
    """
    AI-powered product search using TF-IDF similarity.
    """

    products = list(
        Product.objects
        .select_related("category")
        .filter(stock__gt=0)
    )

    if not query or not products:
        return []

    product_texts = []

    for product in products:
        text = (
            f"{product.name} "
            f"{product.category.name} "
            f"{product.description}"
        )
        product_texts.append(text)

    documents = product_texts + [query]

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents)

    query_vector = matrix[-1]
    product_vectors = matrix[:-1]

    scores = cosine_similarity(
        query_vector,
        product_vectors
    )[0]

    ranked_products = sorted(
        zip(products, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        product
        for product, score in ranked_products[:limit]
        if score > 0
    ]