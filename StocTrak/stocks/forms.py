from django import forms
from .models import Stock

class TickerForm(forms.Form):
    ticker = forms.CharField(label="Ticker ",max_length=5)

class StockForm(forms.ModelForm):
    class Meta:
        model=Stock
        fields = ["ticker"]
    # ticker = forms.CharField(label="Ticker ",max_length=5)
    # class Meta:
    #     model=Stock
    #     fields = ['ticker']