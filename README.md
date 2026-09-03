# 🛒 AI Shop — AI-Powered E-Commerce Platform

AI Shop is a Django-based e-commerce web application designed to provide a complete online shopping experience with intelligent product recommendations, search, wishlist, cart, checkout, order management, and analytics.

The project combines traditional e-commerce functionality with AI-based features to provide a more personalized shopping experience.

---

## 🚀 Features

### 👤 User Authentication
- User Registration
- Secure Login & Logout
- Email Verification
- Password-based authentication
- Protected user-specific pages

### 🛍️ Product Management
- Product listing
- Product detail pages
- Product categories
- Product images
- Stock management
- Product availability tracking

### 🔎 Smart Product Search
- Keyword-based product search
- AI-powered smart search
- Search result ranking
- "No products available" handling

### 🎯 Product Filtering & Sorting
- Category filtering
- Minimum price filtering
- Maximum price filtering
- Price: Low to High
- Price: High to Low
- Newest products
- Oldest products

### ❤️ Wishlist
- Add products to wishlist
- Remove products from wishlist
- User-specific wishlist
- Wishlist product status

### 🛒 Shopping Cart
- Add products to cart
- Increase/decrease quantity
- Remove products
- Automatic subtotal calculation
- Automatic total calculation
- Stock validation

### 📦 Checkout & Orders
- Delivery information
- Order placement
- Order summary
- Stock deduction after purchase
- Order status tracking
- My Orders section
- User-specific order access

### 🤖 AI Recommendations
- Similar product recommendations
- User activity-based recommendations
- Recommendation based on browsing and shopping activity
- Product interaction tracking

### 📊 Analytics Dashboard
- Total users
- Total products
- Total orders
- Revenue information
- Order status analytics
- Product interaction analytics

### 🔐 Security
- Django authentication
- Login-protected pages
- User-specific wishlist
- User-specific orders
- Order ownership validation
- Stock validation
- Environment variables for sensitive credentials
- `.env` excluded from GitHub

### 📱 Responsive UI
- Desktop-friendly interface
- Mobile-friendly navigation
- Responsive product grids
- Responsive checkout and order pages

---

## 🧠 AI / Intelligent Features

AI Shop includes intelligent functionality to improve product discovery and personalization.

### Smart Search

The application processes user search queries and returns relevant products using intelligent search logic.

### Personalized Recommendations

The recommendation system uses user interactions such as:

- Product views
- Cart activity
- Purchases

These interactions are used to generate more relevant product recommendations.

---

## 🛠️ Tech Stack

### Backend
- Python
- Django

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- SQLite

### AI / Recommendation
- Python-based recommendation logic
- User interaction tracking
- Smart product search

### Authentication & Email
- Django Authentication
- Gmail SMTP
- Email Verification

### Development Tools
- Visual Studio Code
- Git
- GitHub

---

## 📁 Project Structure

```text
ai-ecommerce/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── analytics/
│   └── ...
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── orders/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── products/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── recommendations/
│   ├── models.py
│   ├── recommender.py
│   └── ...
│
├── wishlist/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── accounts/
│   ├── analytics/
│   ├── orders/
│   ├── products/
│   └── wishlist/
│
├── .gitignore
├── manage.py
└── requirements.txt
## 👨‍💻 Author

**Abhishek Kumar Pathak**

GitHub: https://github.com/Abhishekkp421
