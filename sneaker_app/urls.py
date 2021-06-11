from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('contact', views.contact),
    path('user_profile/<int:id>', views.profile),
    path('edit/<int:id>', views.edit),
    path('<int:user_id>/delete', views.delete),
    path("purchase",views.purchase),
    path("checkout", views.checkout),
    # path('config/', views.stripe_config),
    # path('create-checkout-session/', views.create_checkout_session),
]