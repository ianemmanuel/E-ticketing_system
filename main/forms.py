from django import forms
from django.forms import widgets
from datetime import date
from .models import Event, EventAttribute, EventReview


class PostForm(forms.ModelForm):
  class Meta:
    model = Event
    fields = ('title','author','Police_Clearance_Form','slug','detail','specs','category','location')

    widgets={
      'title': forms.TextInput(attrs={'class':'form-control'}),
      'author': forms.TextInput(attrs={'class':'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
      # 'author': forms.Select(attrs={'class':'form-control'}),
      'slug': forms.TextInput(attrs={'class':'form-control', 'type':'hidden'}),
      'detail': forms.Textarea(attrs={'class':'form-control'}),
      'specs': forms.Textarea(attrs={'class':'form-control'}),
      'category': forms.Select(attrs={'class':'form-control'}),
      # 'status': forms.CheckboxInput(attrs={'class':'form-check'}),
      # 'is_featurd': forms.CheckboxInput(attrs={'class':'form-check'}),
      'location': forms.Select(attrs={'class':'form-control'}),

    }

class PostAttributeForm(forms.ModelForm):
  class Meta:
    model = EventAttribute
    fields = ('event','price','date','venue','image','video',)
    widgets={
    'venue': forms.TextInput(attrs={'class':'form-control'}),
    'event': forms.Select(attrs={'class':'form-control'}),
    # 'ticket_type': forms.Select(attrs={'class':'form-control'}),
    'price': forms.NumberInput(attrs={'class':'form-control'}),
    'date': forms.NumberInput(attrs={'type':'date'}),

    # 'image': forms.ImageField(attrs={'class':'form-control', 'id':'formFile'}),
    # 'video': forms.FileField(attrs={'class':'form-control-file'}),



  }

# class PostAttributeForm(forms.ModelForm):
#   # event = forms.Select(attrs={'class':'form-control'})
#   event = forms.TextInput(attrs={'class':'form-control', 'value':'', 'id':'manu', 'type':'hidden'}),
#   ticket_type = forms.Select(attrs={'class':'form-select'})
#   price = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
#   date = forms.DateTimeField(widget = forms.NumberInput(attrs={'type':'date'}))
#   # image = forms.FileField(widget=forms.ImageField(attrs={'class':'form-control','type':'file'}))
#   # video = forms.FileField(widget=forms.FileField(attrs={'class':'form-control','type':'file'}))



#   class Meta:
#     model = EventAttribute
#     fields = ('event','ticket_type','price','date','image','video')




# CODE ARTISAN LAB
# Review Add Form
class ReviewAdd(forms.ModelForm):
  class Meta:
    model=EventReview
    fields=('review_text','review_rating')


