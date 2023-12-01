from django import forms

from .models import Listing

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ("title",'description','startBid','imageURL','category')
