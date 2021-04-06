from  django import forms

from .models import Product


class addproductform(forms.ModelForm):
     class Meta:
        model=Product
        fields=['PRDName','PRDCategory','PRDDesc','PRDImage','PRDPrice','PRDDiscountPrice','PRDCost']

