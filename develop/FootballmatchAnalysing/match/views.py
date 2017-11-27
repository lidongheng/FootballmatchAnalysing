#coding:utf-8
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext

# Create your views here.
def index(request):
    #publisher_list = Publisher.objects.filter(country="U.S.A.", state_province="CA")
    t = get_template('match/index.html')
    html = t.render(Context({'saysomething': 'Welcome to Bootstrap World!'}))
    return HttpResponse(html)
