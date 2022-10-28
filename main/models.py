from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import random
from django.shortcuts import render

# DIFFERENT USER LOGINS
from django.contrib.auth.models import AbstractUser



class Banner(models.Model):
    img=models.ImageField(upload_to="banner_imgs/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='1. Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text



class Category(models.Model):
  title = models.CharField(max_length=100)
  image = models.ImageField(upload_to="cat_imgs/")
  description = models.TextField(blank=True, null=True)

  class Meta:
        verbose_name_plural='2. Categories'

  def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

  def __str__(self):
    return self.title

# class Date(models.Model):
#     due_date=models.DateTimeField(editable=True)


#     class Meta:
#         verbose_name_plural='2. Date'

#     # def color_bg(self):
#     #     return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

#     def __str__(self):
#         return self.due_date

# Size

class Location(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="brand_imgs/")

    class Meta:
        verbose_name_plural='3. Locations'

    def __str__(self):
        return self.title


class TicketType(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='4. Types'

    def __str__(self):
        return self.title



class Event(models.Model):
  title=models.CharField(max_length=200)
  author=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  slug=models.CharField(max_length=400,null=True, blank=True, default='ticketshop')
  detail=RichTextField(blank=True, null=True)
  specs=models.TextField()
  category=models.ForeignKey(Category,on_delete=models.CASCADE)
  Police_Clearance_Form= models.FileField(upload_to="clearance_uploaded/",null=True, blank=True)
  status=models.BooleanField(default=True)
  is_featured=models.BooleanField(default=False)
  status=models.BooleanField(default=True)
  location=models.ForeignKey(Location,on_delete=models.CASCADE)
  qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)




  class Meta:
        verbose_name_plural='5. Events'

  def __str__(self):
        return self.title + ' | ' + str(self.author)

  def get_absolute_url(self):
    # return reverse('add_post_attributes',args=(str(self.id)))
    return reverse('add_post_attributes')


  def save(self,*args,**kwargs):
    rno = random.randint(66969,66979)
    qr_image= qrcode.make(rno)
    canvas = Image.new('RGB',(290,290), 'white')
    draw = ImageDraw.Draw(canvas)
    canvas.paste(qr_image)
    fname = f'qr_code-{rno}.png'
    buffer = BytesIO()
    canvas.save(buffer,'PNG')
    self.qr_code.save(fname, File(buffer), save=False)
    canvas.close()
    super().save(*args,**kwargs)
    # Event.objects.otp.append(rno)
    return rno







class EventAttribute(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    venue = models.CharField(max_length=2000, blank=True, null=True)
    # ticket_type=models.ForeignKey(TicketType,on_delete=models.CASCADE)
    price=models.PositiveIntegerField(default=0)
    date=models.DateTimeField(editable=True, blank=True, null=True)
    image=models.ImageField(upload_to="event_imgs/",null=True)
    video = models.FileField(upload_to="videos_uploaded/",null=True, blank=True)



    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    class Meta:
        verbose_name_plural='6. EventAttributes'

    def __str__(self):
        return self.event.title

    def get_absolute_url(self):
    #   return reverse('event_detail',args=(str(self.id)))
        return reverse('home')

# Order
class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amt=models.FloatField()
    paid_status=models.BooleanField(default=False)
    order_dt=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='7. Orders'

# Order Items
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

    class Meta:
        verbose_name_plural='8. OrderItems'

# Product Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class EventReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.review_rating

    def get_absolute_url(self):
        return reverse('home')



class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio=models.TextField()
    profile_pic = models.ImageField(upload_to="profile_imgs/",null=True, blank=True)
    facebook_url=models.CharField(max_length=200, blank=True, null=True)
    instagram_url=models.CharField(max_length=200, blank=True, null=True)
    twitter_url=models.CharField(max_length=200, blank=True, null=True)
    website_url=models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural='9. Profile'

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('home')

# WishList
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'






