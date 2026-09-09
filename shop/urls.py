from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),

    # Башкы бет
    path('', views.home, name='home'),

    # Китептер
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('add/', views.add_book, name='add_book'),

    # Избранное
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('book/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),

    # Корзина
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'), # Бул жерде add_to_cart!
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    # Төлөм
    path('checkout/', views.checkout, name='checkout'),
    path('cart/increase/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),

]




