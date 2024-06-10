from django import forms
from .models import PurchaseOrderItem

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['item', 'quantity', 'price']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }