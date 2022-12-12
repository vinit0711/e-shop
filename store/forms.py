
# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import Customer

# create a ModelForm


class CustomerForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Customer
        fields = "__all__"
