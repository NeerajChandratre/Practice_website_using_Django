from django import forms
from .models import PizzaOrder
class PizzaOrderForm(forms.ModelForm):
    class Meta:
        model = PizzaOrder
        fields = ["customer_name","user_descriptn"]
        widgets = {
            "user_descriptn": forms.Textarea(attrs={"placeholder":"Describe your pizza...spicy/healthy/cheesy etc"}),
        }
        

