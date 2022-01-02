from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .forms import TickerForm
from .tiingo import get_meta_data, get_price_data

# Create your views here.
from django.http import HttpResponse
from .forms import TickerForm

def index(request):
    if request.method == 'POST':
        form=TickerForm(request.POST)
        if form.is_valid():
            ticker=request.POST['ticker']
            return HttpResponseRedirect(ticker)
    else:
        form=TickerForm()
    return render(request, 'index.html',{'form':form})

def ticker(request,tid):
    context = {}
    context['ticker']=tid
    context['meta']=get_meta_data(tid)
    context['price']=get_price_data(tid)
    return render(request,'ticker.html',context)