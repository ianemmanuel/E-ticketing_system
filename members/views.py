from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse,HttpResponse
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm, EditProfilePageForm
from main.models import Profile, CartOrder, CartOrderItems, Wishlist, Event, EventReview
from django.db.models import Max,Min,Count,Avg
from django.template.loader import render_to_string


class UserRegisterView(generic.CreateView):
  form_class = SignUpForm
  template_name = 'registration/register.html'
  success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
  form_class = EditProfileForm
  template_name = 'registration/edit_profile.html'
  success_url = reverse_lazy('home')

  def get_object(self):
    return self.request.user

class PasswordsChangeView(PasswordChangeView):
  form_class = PasswordChangingForm
  # form_class = PasswordChangeForm
  success_url = reverse_lazy('password_success')
  # success_url = reverse_lazy('login')

def password_success(request):
  return render(request, 'registration/password_success.html',{})

class ShowProfilePageView(DetailView):
  model = Profile
  template_name = 'registration/user_profile.html'

  def get_context_data(self, *args, **kwargs):
    # users = Profile.objects.all()
    context = super(ShowProfilePageView, self).get_context_data(*args,**kwargs)
    page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
    context["page_user"] = page_user
    return context

class EditProfilePageView(generic.UpdateView):
  model = Profile
  template_name = 'registration/edit_profile_page.html'
  form_class =  EditProfilePageForm

  success_url = reverse_lazy('my_dashboard')

class CreateProfilePageView(CreateView):
  model = Profile
  template_name = 'registration/create_user_profile_page.html'
  form_class = ProfilePageForm
  success_url = reverse_lazy('my_dashboard')


  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


# User Dashboard
def my_dashboard(request):

  return render(request,'registration/dashboard.html')

# My Orders
def my_orders(request):
	orders=CartOrder.objects.filter(user=request.user).order_by('-id')
	return render(request, 'registration/orders.html',{'orders':orders})

# Order Detail
def my_order_items(request,id):
	order=CartOrder.objects.get(pk=id)
	orderitems=CartOrderItems.objects.filter(order=order).order_by('-id')
	return render(request, 'registration/order-items.html',{'orderitems':orderitems})

# Wishlist
def add_wishlist(request):
    pid=request.GET['event']
    event=Event.objects.get(pk=pid)
    data={}
    checkw=Wishlist.objects.filter(event=event,user=request.user).count()

    if checkw > 0:
      data={
        'bool':False
      }
    else:
      wishlist=Wishlist.objects.create(
        event=event,
        user=request.user
      )
      data={
        'bool':True
      }
    return JsonResponse(data)

# My Wishlist
def my_wishlist(request):
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'registration/wishlist.html',{'wlist':wlist})


# My Reviews
def my_reviews(request):
	reviews=EventReview.objects.filter(user=request.user).order_by('-id')
	return render(request, 'registration/reviews.html',{'reviews':reviews})
