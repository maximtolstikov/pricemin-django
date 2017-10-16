from django import forms
from django.forms import ModelForm
from pricemin.models import Town, Adress, Product, Events
from django.views.generic.edit import UpdateView

class TownForm(ModelForm):
    class Meta:
        model=Town
        fields = ['prefix', 'town_name', 'region', 'user_id']
        widgets = {'region': forms.HiddenInput(), 'user_id': forms.HiddenInput()}

class AdressForm(ModelForm):
    class Meta:
        model=Adress
        fields = ['prefix', 'street', 'number', 'adress_name', 'town', 'user_id'] 
        widgets = {'town': forms.HiddenInput(), 'user_id': forms.HiddenInput()}

class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields = ['product_name', 'product_weight', 'product_price', 'adress', 'user_id']
        widgets = {'adress': forms.HiddenInput(), 'user_id': forms.HiddenInput()}

class EventsForm(ModelForm):
    class Meta:
        model=Events
        fields = ['prefix', 'eventWhere', 'eventComment', 'town', 'eventStart', 'eventStop', 'user_id']
        widgets = {'town': forms.HiddenInput(), 'user_id': forms.HiddenInput()}
