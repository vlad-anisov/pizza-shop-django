from django.urls import path
from .views import IndexView, PizzaView, CartView, DrinksView, OrderView, ProfileView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/pizza', PizzaView.as_view()),
    path('api/pizza/<slug>', PizzaView.as_view()),
    path('api/cart', CartView.as_view()),
    path('api/cart/<int:pk>', CartView.as_view()),
    path('drinks', DrinksView.as_view(), name='drinks'),
    path('order', OrderView.as_view(), name='order'),
    path('profile', ProfileView.as_view(), name='profile'),
]
