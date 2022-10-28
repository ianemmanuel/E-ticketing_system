
from django.shortcuts import render, get_object_or_404
from .models import Category, EventReview, Location, EventAttribute, Event, TicketType, Banner, CartOrder,CartOrderItems, Wishlist
from django.db.models import Max,Min,Count,Avg
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView
from .forms import PostForm, ReviewAdd, PostAttributeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.sessions.models import Session
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
#Recommendation
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# Tickets
import random
import qrcode
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
from members.decorators import allowed_users, admin_only
from .utils import render_to_pdf
from django.views.generic import View




def home(request):
  banners=Banner.objects.all().order_by('-id')
  data=Event.objects.filter(is_featured=True).order_by('-id')
  return render(request, 'index.html',{'data':data, 'banners':banners})

# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})


# Location
def location_list(request):
    data=Location.objects.all().order_by('-id')
    return render(request,'location_list.html',{'data':data})

# Product List
def event_list(request):
  total_data=Event.objects.count()
  data=Event.objects.all().order_by('-id')[:3]
  min_price=EventAttribute.objects.aggregate(Min('price'))
  max_price=EventAttribute.objects.aggregate(Max('price'))


  return render(request,'event_list.html',
		{
			'data':data,
      'max_price':max_price,
      'min_price':min_price,
      'total_data':total_data,
		}
		)
# Product List According to Category
def category_event_list(request,cat_id):
  category=Category.objects.get(id=cat_id)
  data=Event.objects.filter(category=category).order_by('-id')


  return render(request,'category_event_list.html',{'data':data, 'category':category})

# Product List According to Location
def location_event_list(request,location_id):
  location=Location.objects.get(id=location_id)
  data=Event.objects.filter(location=location).order_by('-id')


  return render(request,'location_event_list.html',{'data':data, 'location':location})

#event detail
@login_required(login_url='login')
def event_detail(request,slug,id):
		event=Event.objects.get(id=id)
		related_events=Event.objects.filter(category=event.category).exclude(id=id)[:4]
		# ticket_types=EventAttribute.objects.filter(event=event).values('ticket_type__id','ticket_type__title','price').distinct()
		reviewForm=ReviewAdd()
		# Check
		canAdd=True
		reviewCheck=EventReview.objects.filter(user=request.user,event=event).count()
		if request.user.is_authenticated:
			if reviewCheck > 0:
				canAdd=False
		# End
			# Fetch reviews
		reviews=EventReview.objects.filter(event=event)
		# End

		# Fetch avg rating for reviews
		avg_reviews=EventReview.objects.filter(event=event).aggregate(avg_rating=Avg('review_rating'))
		# End

		return render(
			request, 'event_detail.html',
		{
		'data':event,
		'related':related_events,
		# 'ticket_types':ticket_types,
		'reviewForm':reviewForm,
		'canAdd':canAdd,
		'reviews':reviews,
		'avg_reviews':avg_reviews
		}
		)

@login_required(login_url='login')
# Search
def search(request):
	q=request.GET['q']
	data=Event.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'search.html',{'data':data})


# Filter Data
def filter_data(request):
	categories=request.GET.getlist('category[]')
	locations=request.GET.getlist('location[]')
	# # sizes=request.GET.getlist('size[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allEvents=Event.objects.all().order_by('-id').distinct()
	allEvents=allEvents.filter(eventattribute__price__gte=minPrice)
	allEvents=allEvents.filter(eventattribute__price__lte=maxPrice)
	if len(categories)>0:
		allEvents=allEvents.filter(category__id__in=categories).distinct()
	if len(locations)>0:
		allEvents=allEvents.filter(location__id__in=locations).distinct()
	t=render_to_string('ajax/event-list.html',{'data':allEvents})
	return JsonResponse({'data':t})


# Load More
def load_more_data(request):
  offset=int(request.GET['offset'])
  limit=int(request.GET['limit'])
  data=Event.objects.all().order_by('-id')[offset:offset+limit]
  t=render_to_string('ajax/event-list.html',{'data':data})
  return JsonResponse({'data':t})

# Add to cart
def add_to_cart(request):
	# del request.session['cartdata']
	cart_p={}
	cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'title':request.GET['title'],
		'qty':request.GET['qty'],
		'price':request.GET['price'],
	}
	if 'cartdata' in request.session:
		if str(request.GET['id']) in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
			cart_data.update(cart_data)
			request.session['cartdata']=cart_data
		else:
			cart_data=request.session['cartdata']
			cart_data.update(cart_p)
			request.session['cartdata']=cart_data
	else:
		request.session['cartdata']=cart_p
	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

# Cart List Page
def cart_list(request):
	total_amt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
		return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	else:
		return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})


# Delete Cart Item
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Delete Cart Item
def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

#Checkout
@login_required(login_url='login')
def checkout(request):
	#Process Payment
	# order_id='123'

	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():

			pass
			# Order
		order=CartOrder.objects.create(
				user=request.user,
				total_amt=totalAmt
			)
		# End
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
			# OrderItems
			items=CartOrderItems.objects.create(
				order=order,
				invoice_no='INV-'+str(order.id),
				item=item['title'],
				image=item['image'],
				qty=item['qty'],
				price=item['price'],
				total=float(item['qty'])*float(item['price'])
				)
			# End



		host= request.get_host()
		paypal_dict = {
			'business': settings.PAYPAL_RECIEVER_EMAIL,
			'amount': total_amt,
			'item_name':'OrderNo-'+str(order.id),
			'invoice':'INV-'+str(order.id),
			'currency_code' : 'USD',
			'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
			'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
			'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
		}
		form = PayPalPaymentsForm(initial=paypal_dict)
		return render(request, 'checkout.html',{'items':items, 'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'form': form})



@csrf_exempt
def return_home(request):
	returnData=request.POST
		#Process Payment
	# order_id='123'

	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			# total_amt+=int(item['qty'])*float(item['price'])
			pass
			# Order
		order=CartOrder.objects.create(
				user=request.user,
				total_amt=totalAmt
			)
		# End
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
			# OrderItems
			items=CartOrderItems.objects.create(
				order=order,
				invoice_no='INV-'+str(order.id),
				item=item['title'],
				image=item['image'],
				qty=item['qty'],
				price=item['price'],
				total=float(item['qty'])*float(item['price'])
				)
		Session.objects.all().delete()
		return render(request, 'index.html')



@csrf_exempt
def payment_done(request):
	returnData=request.POST
		#Process Payment
	# order_id='123'

	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			# total_amt+=int(item['qty'])*float(item['price'])
			pass
			# Order
		order=CartOrder.objects.create(
				user=request.user,
				total_amt=totalAmt
			)
		# End
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
			# OrderItems
			items=CartOrderItems.objects.create(
				order=order,
				invoice_no='INV-'+str(order.id),
				item=item['title'],
				image=item['image'],
				qty=item['qty'],
				price=item['price'],
				total=float(item['qty'])*float(item['price'])
				)
			# End

		return render(request, 'payment-success.html',{'items':items, 'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})



@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')

# Save Review
def save_review(request,pid):
	event=Event.objects.get(pk=pid)
	user=request.user
	review=EventReview.objects.create(
		user=user,
		event=event,
		review_text=request.POST['review_text'],
		review_rating=request.POST['review_rating'],
		)
	data={
		'user':user.username,
		'review_text':request.POST['review_text'],
		'review_rating':request.POST['review_rating']
	}

	# Fetch avg rating for reviews
	avg_reviews=EventReview.objects.filter(event=event).aggregate(avg_rating=Avg('review_rating'))
	# End

	return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})


def ticket_view(request,pid):
	event=Event.objects.get(pk=pid)
	image=EventAttribute.objects.filter(event=event).values('image').distinct

	template_path = 'pdf1.html'
	context = {'event': event, 'image':image}
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
	template = get_template(template_path)
	html = template.render(context)

	# create a pdf
	pisa_status = pisa.CreatePDF(
			html, dest=response,)

	if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response



# Upload event class View

# @method_decorator(admin_only, name='dispatch')
class AddPostView(CreateView):
  model= Event
  form_class= PostForm
  template_name = 'add_post.html'
  # fields= '__all__'

class AddPostAttributesView(CreateView):
	model = EventAttribute
	template_name = 'add_post_attributes.html'
	form_class = PostAttributeForm

class ViewPost(ListView):
	model = Event
	template_name = 'my_events.html'



def verifyticket(request, pid):
		event=Event.objects.get(pk=pid)
		image=EventAttribute.objects.filter(event=event).values('image').distinct
		tickets= [66969,66970,66971,66972,66973,66973,66974,66975,66976,66977,66978,66979]
		my_tickets = [str(item) for item in tickets]
		otp = event.save()
		user_otp1 = request.POST.get("otp")
		# message = validateOTP(user_otp1)
		if user_otp1 in my_tickets:
			return render(request, 'verify_tickets.html', {"message1": "Valid Ticket",'event': event,'image':image})
		else:
			return render(request, 'verify_tickets.html', {"message2": "Invalid Ticket",'event': event,'image':image})


def recommendation(request):
	pid=request.GET['event']
	event=Event.objects.get(pk=pid)
	wishlist=Wishlist.objects.filter(event=event, user=request.user).order_by('-id')

	checkw=Wishlist.objects.filter(event=event,user=request.user).count()

	# from google.colab import files
	# uploaded = files.upload()
	df = pd.read(wishlist)
	df.head(3)
	 # Get a count of the number of rows/ movies in the data set and the number of columns
	df.shape
		# Create a list of important columns for the recommendation engine
	columns = ['Category', 'Price','Location','author','title']
		# Show the data
	df[columns].head(3)
		# Check for any missing values in the important columns
	df[columns].isnull().values.any()

	#	 Create a function to combine the values of the important columns into a single string
	def get_important_features(data):
		important_features = []
		for i in range(0, data.shape[0]):
			important_features.append(data['Category'][i]+data['Price'][i]+data['Location'][i]+data['author'][i]+data['title'][i])
		return important_features

	df ['important_features'] = get_important_features(df)

	df.head(3)

	cm = CountVectorizer().fit_transform(df['important_features'])

# Get the cosine similarity matrix from the count matrix
	cs= cosine_similarity(cm)
	print(cs)
	
	cs.shape
	predictor_event = wishlist

	movie_id = df[df.Title==predictor_event]['Event_id'].values[0]
	scores = list(enumerate(cs[movie_id]))
	sorted_scores = sorted(scores, key = lambda x:x[1], reverse = True)
	sorted_scores = sorted_scores[1:]
	print(sorted_scores)
	j = 0
	print('The 7 most recommended movies are: ')
	for item in sorted_scores:
		movie_title = df[df.Movie_id == item[0]]['Title'].values[0]
		print(j+1, movie_title)
		j = j+1
		if j>4:
			break
	return render(request, 'event_detail.html',{'movie_title':movie_title})


# Wishlist
def add_wishlist(request):
	pid=request.GET['product']
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



