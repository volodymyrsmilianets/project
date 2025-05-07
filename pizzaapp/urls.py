from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:cat_id>/', views.category_products, name='category_products'),
    path('product/<int:prod_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:prod_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:prod_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<int:order_id>/receipt/', views.order_receipt, name='order_receipt'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('favorites/add/<int:prod_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:prod_id>/', views.remove_from_favorites, name='remove_from_favorites'),
]