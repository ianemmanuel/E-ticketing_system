from django.contrib import admin
from .models import Banner, Category, TicketType,Event,EventAttribute, Location, Profile, CartOrder, CartOrderItems, EventReview, Wishlist

admin.site.register(TicketType)
admin.site.register(Location)
admin.site.register(Profile)


class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class CategoryAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display=('id','title','author','category','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Event,EventAdmin)

class EventAttributeAdmin(admin.ModelAdmin):
    list_display=('id','image_tag','event','price','date')
admin.site.register(EventAttribute,EventAttributeAdmin)

# Order
class CartOrderAdmin(admin.ModelAdmin):
	# list_editable=('paid_status','order_status')
	list_display=('user','total_amt','paid_status','order_dt')
admin.site.register(CartOrder,CartOrderAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
	list_display=('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)

admin.site.register(Wishlist)


class EventReviewAdmin(admin.ModelAdmin):
	list_display=('user','event','review_text','get_review_rating')
admin.site.register(EventReview,EventReviewAdmin)





