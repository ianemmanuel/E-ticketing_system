from django.urls import path, include
from . import views
from .views import AddPostView, AddPostAttributesView, ViewPost

# from members.views import add_wishlist, my_wishlist

from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
  path('',views.home,name='home'),
  path('members/',include('members.urls')),
  path('search',views.search,name='search'),
  path('category-list',views.category_list,name='category-list'),
  path('location-list',views.location_list,name='location-list'),
  path('event-list',views.event_list,name='event-list'),
  path('category-event-list/<int:cat_id>',views.category_event_list,name='category-event-list'),
  path('location-event-list/<int:location_id>',views.location_event_list,name='location-event-list'),
  path('event/<str:slug>/<int:id>',views.event_detail,name='event_detail'),
  path('filter-data',views.filter_data,name='filter-data'),
  path('load-more-data',views.load_more_data,name='load_more_data'),
  path('add-to-cart',views.add_to_cart,name='add_to_cart'),
  path('cart',views.cart_list,name='cart'),
  path('add_post/',AddPostView.as_view(),name='add_post'),
  path('add_post_attributes/',AddPostAttributesView.as_view(),name='add_post_attributes'),
  path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
  path('update-cart',views.update_cart_item,name='update-cart'),
  path('checkout',views.checkout,name='checkout'),
  path('paypal/', include('paypal.standard.ipn.urls')),
  path('payment-done/', views.payment_done, name='payment_done'),
  path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
  path('save-review/<int:pid>',views.save_review, name='save-review'),
  path('ticket-view/<str:pid>',views.ticket_view, name='ticket-view'),
  path('my_events', ViewPost.as_view(), name='my_events'),
  path('verify_tickets/<str:pid>',views.verifyticket, name='verify_tickets'),
  path('add-wishlist',views.add_wishlist, name='add_wishlist'),
  path('',views.return_home,name='home2')


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
