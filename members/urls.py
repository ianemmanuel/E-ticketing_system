from django.urls import path
from .views import UserRegisterView, UserEditView, PasswordsChangeView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
  path('register/', UserRegisterView.as_view(), name='register'),
  path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
  # path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
  path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
  path('password_success', views.password_success, name="password_success"),
  path('<int:pk>/profile/', ShowProfilePageView.as_view(), name= 'show_profile_page'),
  path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name= 'edit_profile_page'),
  path('create_profile_page/', CreateProfilePageView.as_view(), name= 'create_profile_page'),
  # User Section start
  path('my-dashboard',views.my_dashboard, name='my_dashboard'),
  path('my-orders',views.my_orders, name='my_orders'),
  path('my-orders-items/<int:id>',views.my_order_items, name='my_order_items'),

  path('my-reviews',views.my_reviews, name='my-reviews'),
  # End
  # Wishlist
  path('add-wishlist',views.add_wishlist, name='add_wishlist'),
  path('my-wishlist',views.my_wishlist, name='my_wishlist'),



]
