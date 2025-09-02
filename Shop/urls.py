from django.urls import path
from . import views 

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Add login URL pattern
    path('logout/', views.logout_view, name='logout'),  # Add logout URL pattern
    path('home/', views.home, name='home'),
    path('products/', views.products_index, name='products_index'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:name>/', views.categoriesview, name='categoriesview'),
    path('categories/<str:cname>/<str:pname>/', views.product_details, name='product_details'),
    path('addtocart/', views.add_to_cart, name='addtocart'),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),  # Add wishlist view URL
    path('remove_from_wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    # New URL patterns for About and Contact
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
