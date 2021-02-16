import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main_app.models import CustomUser,Otp
from django.views.decorators.csrf import csrf_exempt
from main_app.AuthBackend import AuthBackend 
import random


def login(request):
    return render(request,"user_template/login.html")

def verify_login(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=AuthBackend.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            if user.is_active==True:
                log_in(request,user)
                if user.user_type=="1":
                    return HttpResponseRedirect('/dashboard')
                else:
                    return HttpResponseRedirect(reverse("home"))
            else:
                messages.error(request,"Your Account Is Disable ! Contact Company Owner")
                return HttpResponseRedirect(reverse('login'))

        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect(reverse('login'))

def logout(request):
    log_out(request)
    return HttpResponseRedirect(reverse('home'))

def forget_password(request):
    return render(request,"user_template/forget_password.html")

def forget_password_otp_send(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        email = request.POST.get("email")
        if email != '':
            try:
                user = CustomUser.objects.filter(email = email).exists()
                if user:
                    u_id = CustomUser.objects.get(email = email).id
                    cust_instance = CustomUser.objects.get(id=u_id)
                    otp= random.randint(100000,999999)
                    otp_old = Otp.objects.filter(cust_id = u_id).exists()
                    if otp_old:
                        otp_old = Otp.objects.get(cust_id = u_id).delete()
                    print('otp otp',otp)

                    otp = Otp(otp =otp , cust_id =cust_instance)
                    otp.save()

                    context={
                        "otp":otp,
                        "u_id":u_id
                    }
                    messages.success(request,"OTP Send")
                    return render(request,"user_template/forget_password_otp.html",context)
                else:
                    messages.error(request,"Incorrect Email")
                    return render(request,"user_template/forget_password.html",{"email":email})
            except Exception as e:
                messages.error(request,"Something Wnet Wrong Try Later {}".format(e))
                return render(request,"user_template/forget_password.html",{"email":email})
        else:
            messages.error(request,"Please Fill The Email Filed")
            return HttpResponseRedirect(reverse('forget_password'))

def forget_password_otp_verify(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        otp = request.POST.get("otp")
        u_id = request.POST.get("u_id")
        if otp != '':
            try:
                o_t_p = Otp.objects.get(cust_id = u_id)
                original_otp = o_t_p.otp
                print('original_otp',original_otp)
                if int(original_otp) == int(otp):
                    return render(request,"user_template/set_new_password.html",{"u_id":u_id})
                else:
                    messages.error(request,"Incorrect OTP")
                    return render(request,"user_template/forget_password_otp.html",{"u_id":u_id})
            except Exception as e:
                messages.error(request,"Something Wnet Wrong Try Later {}".format(e))
                return render(request,"user_template/forget_password.html",{"u_id":u_id})
        else:
            messages.error(request,"Please Fill The OTP Filed")
            return HttpResponseRedirect(reverse('forget_password'))
def set_new_password_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        new_password = request.POST.get("new_password")
        new_c_password = request.POST.get("new_c_password")
        u_id = request.POST.get("u_id")
        if new_c_password != '' and new_password != '':
            if new_password  == new_c_password:
                user = CustomUser.objects.get(id=u_id)
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(request,"Confirm Password Not Matched")
                return render(request,"user_template/set_new_password.html",{"u_id":u_id})
        else:
            messages.error(request,"Please Fill  All  The Filed")
            return HttpResponseRedirect(reverse('forget_password'))


