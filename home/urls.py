from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='main_home'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),
    path('order-summary', views.OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('/add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('/remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('/remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/', views.PaymentView.as_view(), name='payment')
]
