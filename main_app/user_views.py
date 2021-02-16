from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
import random
from main_app.models import Customer,Receipt
from datetime import datetime
from django.db import connection
from django.db.utils import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def home(request):
    return render(request,"user_template/index.html")
def user_receipt(request):
    if request.user.is_authenticated:
        u_id = request.user.id
        user = Customer.objects.all()
        for i in user:
            x= i.admin_id
            if int(x) == int(u_id):
                user_id = i.id
        cust_id = user_id
        receipt = Receipt.objects.filter(cust_id=cust_id).order_by('-id')
        return render(request,"user_template/user_receipt.html",{"receipt":receipt})
    else:
        return HttpResponseRedirect(reverse('home'))