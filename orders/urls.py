from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pizza_all/', views.pizza_all, name='all_pizzas'),
    path('pizza_meat/', views.pizza_meat, name='meat_pizzas'),
    path('pizza_veg/', views.pizza_veg, name='veg_pizzas'),
    path('pizza_grill/', views.pizza_grill, name='grill_pizzas'),
    path('pizza_hot/', views.pizza_hot, name='hot_pizzas'),
    path('pizza_closed/', views.pizza_closed, name='closed_pizzas'),

    re_path(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.order_details, name='order_details'),


]