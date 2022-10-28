from .models import Category, Location, EventAttribute, Event, TicketType, Banner
from django.db.models import Min,Max



def get_filters(request):
  cats=Event.objects.distinct().values('category__title','category__id')
  locations=Event.objects.distinct().values('location__title','location__id')
  minMaxPrice=EventAttribute.objects.aggregate(Min('price'),Max('price'))
  data={
      'cats':cats,
      'locations':locations,
      'minMaxPrice': minMaxPrice,
    }
  return data