from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import Stock
from .forms import TickerForm, StockForm
from django.contrib import messages
from .tiingo import get_meta_data, get_price_data

# Create your views here.
from django.http import HttpResponse
from .forms import TickerForm
import requests
import json
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

# def index(request):
#     if request.method == 'POST':
#         form=TickerForm(request.POST)
#         if form.is_valid():
#             ticker=request.POST['ticker']
#             return HttpResponseRedirect(ticker)
#     else:
#         form=TickerForm()
#     return render(request, 'index.html',{'form':form})

# def ticker(request,tid):
#     context = {}
#     context['ticker']=tid
#     context['meta']=get_meta_data(tid)
#     context['price']=get_price_data(tid)
#     return render(request,'ticker.html',context)

def plotlyplot(ticker):
    #for plotly candlestick plot
        data = yf.download(tickers=ticker,period='5y',interval='1d')

        #declare figure
        fig=go.Figure()

        #Candlestick
        fig.add_trace(go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'], name = 'market data'))

        # Add titles
        fig.update_layout(
            title=ticker+' historical share prices',
            yaxis_title='Stock Price (USD per Shares)')

        # X-Axes
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    # dict(count=1, label="1m", step="minute", stepmode="backward"),
                    # dict(count=1, label="1h", step="hour", stepmode="backward"),
                    # dict(count=12, label="12h", step="hour", stepmode="backward"),
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="7d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=3, label="3y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        #Show
        fig.show()
        figure=fig.write_html("./tmpfile.html")

def home(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        content={}
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_062031d20883444f9ea74e2610fe2011")
        try:
            api = json.loads(api_request.content)
            content['meta']=get_meta_data(ticker)
            content['price']=get_price_data(ticker)
        except Exception as e:
            api = "Error..."
        plotlyplot(ticker)  
        return render(request, 'home1.html', {'content':content,'api': api})
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_062031d20883444f9ea74e2610fe2011")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."
        return render(request, 'home1.html', {'ticker': ticker, 'output': output})

def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
	import requests 
	import json 

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added!"))
			return redirect('add_stock')

	else:	
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_062031d20883444f9ea74e2610fe2011")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."
		
		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted!"))
	return redirect(delete_stock)

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})
    