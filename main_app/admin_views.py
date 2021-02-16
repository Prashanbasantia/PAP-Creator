import json
import os
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from main_app.models import CustomUser,Customer,products,Category_prod,Receipt,Img,Otp
import datetime
import random
# from django.views.generic import View


#generate pdf
# from io import BytesIO
# from django.template.loader import get_template
# from xhtml2pdf import pisa

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

def dashboard(request):
    cust = CustomUser.objects.all()
    inac_customer= 0
    ac_customer = 0
    for i in cust:
        if i.is_active == True:
            ac_customer += 1
        if i.is_active == False:
            inac_customer += 1
        
    product = products.objects.all().count()
    today =datetime.datetime.today()
    tran = Receipt.objects.filter(created_at__date=today).count()
    context = {
        "inac_customer":inac_customer,
        "ac_customer":ac_customer,
        "product":product,
        "tran":tran
    }
    return render(request,"admin_template/dashboard.html",context)
def admin_profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    return render(request,"admin_template/profile.html",{"user":user})
def admin_change_name(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        if request.method!="POST":
            return HttpResponse("Method Not Allowed")
        else:
            f_name=request.POST.get("change_f_name")
            l_name=request.POST.get("change_l_name")
            try:
                customuser=CustomUser.objects.get(id=request.user.id)
                customuser.first_name=f_name
                customuser.last_name=l_name
                customuser.save()
                messages.success(request,"Name Change Successfully")
                return HttpResponseRedirect(reverse("admin_profile"))
            except:
                messages.error(request,"Failed To Change Name")
                return HttpResponseRedirect(reverse("admin_profile"))

def admin_change_mobile(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        u_id=request.user.id
        username=request.POST.get("change_mobile")
        email=request.POST.get("change_opt_mobile")
        try:
            customuser=CustomUser.objects.get(id=u_id)
            if customuser.email == email:
                customuser.username=username
                customuser.email=email
                customuser.save()
                messages.success(request,"Mobile Change Successfully")
                return HttpResponseRedirect(reverse("admin_profile"))
            else:
                return render(request,"admin_template/password_verify_change_mobile.html",{"u_id":u_id,"username":username,"email":email})

        except Exception as e:
            messages.error(request,"Failed To Change Mobile")
            return HttpResponseRedirect(reverse("admin_profile"))

def password_verify_admin_change_mobile(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        u_id = request.POST.get('cust_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        UserModel=get_user_model()
        user = UserModel.objects.get(id = u_id)
        if password != '':
            if user.check_password(password):
                cust = CustomUser.objects.get(id = u_id)
                cust.email = email
                cust.username = username
                cust.save()
                return HttpResponseRedirect(reverse("logout"))
            else:
                messages.error(request,"Password Is Wrong")
                return render(request,"admin_template/otp_verify_change_password.html",{"u_id":u_id,'username':username,"email":email})
        else:
            messages.error(request,"Please Fill The Password Filed")
            return render(request,"admin_template/otp_verify_change_password.html",{"u_id":u_id,'username':username,"email":email})

def admin_change_password(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        old_password=request.POST.get("old_password")
        new_password=request.POST.get("new_password")
        new_c_password=request.POST.get("new_c_password")
        u_id = request.user.id
        if old_password != '' and new_c_password != '' and new_c_password != '':
            try:
                if new_password == new_c_password:
                    UserModel=get_user_model()
                    user = UserModel.objects.get(id = u_id)
                    if user.check_password(old_password):
                        customuser=CustomUser.objects.get(id=u_id)
                        customuser.set_password(new_password)
                        customuser.save()
                        return HttpResponseRedirect(reverse("logout"))
                    else:
                        messages.error(request,"Current Password Is Wrong")
                        return HttpResponseRedirect(reverse("admin_profile"))
                else:
                    messages.error(request,"Confirm Password Is Not Matched")
                    return HttpResponseRedirect(reverse("admin_profile"))
            except Exception as e:
                messages.error(request,"Failed To Change Password ")
                return HttpResponseRedirect(reverse("admin_profile"))
                
        else:
            messages.error(request,"Please Fill All The Filed")
            return HttpResponseRedirect(reverse("admin_profile"))


def admin_change_profile_image(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        profile_pic_url=request.FILES.get("profile_photo")
        print(profile_pic_url)
        if profile_pic_url != None:
            try:
                user=CustomUser.objects.get(id=request.user.id)
                old_pic = user.profile_photo
                print("old pic",old_pic)
                if old_pic != '' and profile_pic_url != None:
                    old_pic = str(old_pic)
                    os.remove(os.path.join(settings.MEDIA_ROOT,old_pic))
                user.profile_photo = profile_pic_url
                user.save()
                messages.success(request,"Profile Image Change Successfully")
                return HttpResponseRedirect(reverse("admin_profile"))
            except Exception as e:
                messages.error(request,"Failed To Change Profile Image {}".format(e))
                return HttpResponseRedirect(reverse("admin_profile"))
        else:
            messages.error(request,"Pease Choose An Image")
            return HttpResponseRedirect(reverse("admin_profile"))


def add_product(request):
    cate = Category_prod.objects.all()
    return render(request,"admin_template/add_product.html",{"cate":cate})

def save_product(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        name=request.POST.get("product_name")
        unity=request.POST.get("product_unity")
        price=request.POST.get("product_price")
        cate_id=request.POST.get("product_type")
        cate_instance= Category_prod.objects.get(id = cate_id)
        try:
            p_exist = products.objects.filter(name = name,unity = unity).exists()
            
            if p_exist:
                messages.error(request,"{} of unity {} KG is already Exist".format(name,unity))
                return HttpResponseRedirect(reverse("add_product"))
            else:
                prod=products(name=name,unity=unity, price = price,cate_id = cate_instance)
                prod.save()
                messages.success(request,"{} Added Successfully".format(name))
                return HttpResponseRedirect(reverse("add_product"))
        except Exception as e:
            messages.error(request,"Failed to Add Product {}".format(e))
            return HttpResponseRedirect(reverse("add_product"))


def edit_product(request,prod_id):
    prod = products.objects.get(id = prod_id)
    cate = Category_prod.objects.all()
    return render(request,"admin_template/edit_product.html",{"prod":prod,"cate":cate})



def update_product(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        prod_id=request.POST.get("product_id")
        name=request.POST.get("product_name")
        unity=request.POST.get("product_unity")
        price=request.POST.get("product_price")
        c_id = request.POST.get("product_type")
        cate_id = Category_prod.objects.get(id = c_id)
        try:
            prod=products.objects.get(id=prod_id)
            prod.name=name
            prod.unity = unity
            prod.price = price
            prod.cate_id = cate_id
            prod.save()
            messages.success(request,"{} Updated Successfully".format(name))
            return HttpResponseRedirect(reverse("edit_product",kwargs={"prod_id":prod_id}))
        except:
            messages.error(request,"Failed to Update product")
            return HttpResponseRedirect(reverse("edit_product",kwargs={"prod_id":prod_id}))
def view_product(request):
    prod = products.objects.all().order_by('-id')
    return render(request,"admin_template/view_product.html",{"prod":prod})

def add_category(request):
    cate = Category_prod.objects.all().order_by("-id")
    return render(request,"admin_template/add_category.html",{"cate":cate})

def save_category(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        name=request.POST.get("cate_name")
        try:
            cate=Category_prod(name=name)
            cate.save()
            messages.success(request,"{} Added Successfully".format(name))
            return HttpResponseRedirect(reverse("add_category"))
        except:
            messages.error(request,"Failed to Add Category")
            return HttpResponseRedirect(reverse("add_category"))

def add_customer(request):
    return render(request,"admin_template/add_customer.html")

def save_customer(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name=request.POST.get("f_name")
        last_name=request.POST.get("l_name")
        username=request.POST.get("aaddhar")
        email=request.POST.get("mobile")
        dob=request.POST.get("dob")
        address=request.POST.get("address")
        if first_name !='' and last_name !='' and username !='' and email !='' and dob !='' and address !='':    
            if request.FILES.get('profile_photo'):
                profile_pic_url=request.FILES['profile_photo']
            else:
                profile_pic_url=None
            try:
                unvefi_cust = Customer.objects.filter(is_verify = False)
                for uv in unvefi_cust:
                    cu_id = uv.admin_id
                    cu=CustomUser.objects.get(id= cu_id)
                    profile_image = cu.profile_photo
                    os.remove(os.path.join(settings.MEDIA_ROOT,str(profile_image)))
                    cu.delete()

                cmr=CustomUser.objects.create_user(username=username,password=username,email=email,last_name=last_name,first_name=first_name,user_type=2,profile_photo = profile_pic_url,is_active=False)
                cmr.customer.address=address
                cmr.customer.dob=dob
                cmr.save()
                cust_id =cmr.id
                cust_instance = CustomUser.objects.get(id = cust_id)
                otp = random.randint(100000,999999)
                OTP = Otp(otp=otp,cust_id=cust_instance)
                print("opt is",otp)
                OTP.save()
                return render(request,"admin_template/otp_verify.html",{"cust_id":cust_id,"email":email})
            except:
                messages.error(request,"Failed to Add Customer ")
                return HttpResponseRedirect(reverse("add_customer"))
        else:
            messages.error(request,"Please Fill Al the Fileds ")
            return HttpResponseRedirect(reverse("add_customer"))
def otp_verify(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        cust_id = request.POST.get('cust_id')
        otp = request.POST.get('otp')
        print('get otp',otp)
        ot= Otp.objects.get(cust_id=cust_id)
        orignal_otp = ot.otp
        if otp != '':
            if int(orignal_otp) == int(otp):
                cust = CustomUser.objects.get(id = cust_id)
                email=cust.email
                c_user = Customer.objects.get(admin =cust_id)

                c_user.is_verify = True
                c_user.save()

                cust.is_active = True
                cust.save()
            
                messages.success(request,"Customer Added Successfuly ")
                return HttpResponseRedirect(reverse("add_customer"))
            else:
                messages.error(request," Otp Does Not Match ")
                return render(request,"admin_template/otp_verify.html",{"cust_id":cust_id,"otp":otp,"email":email})
        else:
            messages.error(request,"Please Fill The OTP Filed")
            return render(request,"admin_template/otp_verify.html",{"cust_id":cust_id,"otp":otp})

def edit_customer(request,cust_id):
    cust = Customer.objects.get(admin=cust_id)
    return render(request,"admin_template/edit_customer.html",{"cust":cust})



def update_customer(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        cust_id=request.POST.get("cust_id")
        first_name=request.POST.get("f_name")
        last_name=request.POST.get("l_name")
        username=request.POST.get("aaddhar")
        email=request.POST.get("mobile")
        dob=request.POST.get("dob")
        address=request.POST.get("address")
        inac=request.POST.get("inactive")
        
        if request.FILES.get('profile_photo'):
            profile_pic_url=request.FILES['profile_photo']
        else:
            profile_pic_url=None
        try:
            if inac == "on":
                is_active = True
            if inac == None:
                is_active = False
            user=CustomUser.objects.get(id=cust_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.set_password(username)
            user.is_active = is_active
            
            old_pic = user.profile_photo
            if old_pic != None and profile_pic_url !=None:
                old_pic = str(old_pic)
                os.remove(os.path.join(settings.MEDIA_ROOT,old_pic))
            if profile_pic_url == None:
                user.profile_photo = old_pic 
            else:
                user.profile_photo = profile_pic_url
                
            user.save()

            cmr=Customer.objects.get(admin = cust_id)
            cmr.address=address
            cmr.dob=dob
            cmr.save()
            
            messages.success(request,"{} Updated Successfully".format(first_name))
            return HttpResponseRedirect(reverse("edit_customer",kwargs={"cust_id":cust_id}))
        except:
            messages.error(request,"Failed to Update Customer")
            return HttpResponseRedirect(reverse("edit_customer",kwargs={"cust_id":cust_id}))
def view_customer(request):
    cm = Customer.objects.all().order_by('-id')
    cmr = []
    for i in cm:
        if i.admin.is_active == True and i.is_verify == True:
            cmr.append(i)
    return render(request,"admin_template/view_customer.html",{"cmr":cmr})
def view_inac_customer(request):
    cm = Customer.objects.all().order_by('-id')
    cmr = []
    for i in cm:
        if i.admin.is_active == False:
            cmr.append(i)
    return render(request,"admin_template/view_inactive_customer.html",{"cmr":cmr})

#8328991704
#353892ACah2Z7u60229ab9P1
def delete_customer(request,cust_id):
    cmr = CustomUser.objects.get(id = cust_id)
    cm = cmr.user_type
    print("c_name",cm)
    cmr.delete()
    # if cm =="2":
    #     cmr.delete()
    #     print("dele suc")
    # else:
    #     pass
    return HttpResponseRedirect(reverse("view_customer"))
def add_item(request):
    prod = products.objects.all()
    return render(request,"admin_template/add_item.html",{"prod":prod})
def save_item(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        prod_id=request.POST.get("item_name")
        quant=request.POST.get("item_quant")
        p = products.objects.get(id = prod_id)
        quan = p.quantity
        quantity = int(quan)+int(quant)
        try:
            prod = products.objects.get(id = prod_id)
            prod.quantity = quantity
            prod.save()
            messages.success(request,"{} of Quantity {} Added To  Stock".format(p.quantity,p.name))
            return HttpResponseRedirect(reverse("add_item"))
        except Exception as e:
            messages.error(request,"Failed to Add Product Quantity To Stock {}".format(e))
            return HttpResponseRedirect(reverse("add_item"))

def inventory(request):
    cate = Category_prod.objects.all()
    prod = products.objects.all()
    return render(request,"admin_template/inventory.html",{"cate":cate,"prod":prod})
    
def receipt(request):
    cust = Customer.objects.all()
    prod= products.objects.all()
    return render(request,"admin_template/receipt.html",{"cust":cust,"prod":prod})
def save_receipt(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        receipt_type=request.POST.get("receipt_type")
        prod_id=request.POST.getlist("prod_id")
        cust_id=request.POST.get("cust_id")
        prod_quantity=request.POST.getlist("prod_quantity")
        print(prod_quantity)
        cust_instance = Customer.objects.get(id = cust_id)
        try:
            if receipt_type != '' and prod_quantity != ['']:
                c = min([len(prod_id),len(prod_quantity)])
                for i in range(c):
                    prod_instance = products.objects.get(id = prod_id[i])
                    receipt = Receipt(prod_id= prod_instance, cust_id = cust_instance, prod_quantity=prod_quantity[i],receipt_type=receipt_type)
                    receipt.save()
                    prod = products.objects.get(id = prod_id[i])
                    pq= prod.quantity
                    if receipt_type=='1':
                        quantity = int(pq)-int(prod_quantity[i])
                        prod.quantity = quantity
                        prod.save()
                    elif receipt_type=='0':
                        quantity = int(pq)+int(prod_quantity[i])
                        prod.quantity = quantity
                        prod.save()
                    else:
                        messages.error(request,"Please Choose Product Type")
                        return HttpResponseRedirect(reverse("receipt"))
            else:
                messages.error(request,"Please Fill All The Fileds")
                return HttpResponseRedirect(reverse("receipt"))
                    
            messages.success(request,"Receipt Made  Successfully")
            return HttpResponseRedirect(reverse("receipt"))
        except Exception as e:
            messages.error(request,"Failed To Make Receipt")
            return HttpResponseRedirect(reverse("receipt"))
def transaction(request):
    receipt = Receipt.objects.all().order_by('-id')
    return render(request,"admin_template/transaction.html",{"receipt":receipt})
def cust_tran(request,cust_id):
    receipt = Receipt.objects.filter(cust_id= cust_id)
    return render(request,"admin_template/transaction.html",{"receipt":receipt})

def img(request):
    im = Img.objects.all()
    return render(request,"admin_template/make_receipt.html",{"im":im})
def img_upload(request):
    if request.method !="POST":
        return HttpResponse("hii")
    else:
        if request.FILES.get('file_name'):
            fn=request.FILES['file_name']
            im = Img(profile_photo=fn)
            im.save()
            messages.success(request,"pass to Add Product Quantity To Stock")
            return HttpResponseRedirect(reverse("img"))
        messages.error(request,"Failed to Add Product Quantity To Stock")
        return HttpResponseRedirect(reverse("img"))

@csrf_exempt
def resend_user_otp(request):
    cust_id = request.POST.get('cust_id')
    if cust_id !='':
        re_otp= random.randint(100000,999999)
        print('resend otp',re_otp)
        otp = Otp.objects.get(cust_id = cust_id)
        otp.otp = re_otp
        otp.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)
# def edit_student(request,student_id):
#     request.session['student_id']=student_id
#     student=Students.objects.get(admin=student_id)
#     form=EditStudentForm()
#     form.fields['email'].initial=student.admin.email
#     form.fields['first_name'].initial=student.admin.first_name
#     form.fields['last_name'].initial=student.admin.last_name
#     form.fields['username'].initial=student.admin.username
#     form.fields['address'].initial=student.address
#     form.fields['course'].initial=student.course_id.id
#     form.fields['sex'].initial=student.gender
#     form.fields['session_year_id'].initial=student.session_year_id.id
#     return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

# def edit_student_save(request):
#     if request.method!="POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
#         student_id=request.session.get("student_id")
#         if student_id==None:
#             return HttpResponseRedirect(reverse("manage_student"))

#         form=EditStudentForm(request.POST,request.FILES)
#         if form.is_valid():
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             username = form.cleaned_data["username"]
#             email = form.cleaned_data["email"]
#             address = form.cleaned_data["address"]
#             session_year_id=form.cleaned_data["session_year_id"]
#             course_id = form.cleaned_data["course"]
#             sex = form.cleaned_data["sex"]
#             try:
#                 user=CustomUser.objects.get(id=student_id)
#                 user.first_name=first_name
#                 user.last_name=last_name
#                 user.username=username
#                 user.email=email
#                 user.save()

#                 student=Students.objects.get(admin=student_id)
#                 student.address=address
#                 student.mobile=mobile
#                 student.dob=dob
#                 student.aaddhar=aaddhar
#                 session_year = SessionYearModel.object.get(id=session_year_id)
#                 student.session_year_id = session_year
#                 student.gender=sex
#                 course=Courses.objects.get(id=course_id)
#                 student.course_id=course
#                 del request.session['student_id']
#                 messages.success(request,"Successfully Edited Student")
#                 return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
#             except:
#                 messages.error(request,"Failed to Edit Student")
#                 return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
#         else:
#             form=EditStudentForm(request.POST)
#             student=Students.objects.get(admin=student_id)
#             return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

# def edit_subject(request,subject_id):
#     subject=Subjects.objects.get(id=subject_id)
#     courses=Courses.objects.all()
#     session_year = SessionYearModel.object.all()
#     staffs=CustomUser.objects.filter(user_type=2)
#     return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id,"session_year":session_year})

# def edit_subject_save(request):
#     if request.method!="POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
#         subject_id=request.POST.get("subject_id")
#         subject_name=request.POST.get("subject_name")
#         staff_id=request.POST.get("staff")
#         course_id=request.POST.get("course")

#         try:
#             subject=Subjects.objects.get(id=subject_id)
#             subject.subject_name=subject_name
#             staff=CustomUser.objects.get(id=staff_id)
#             subject.staff_id=staff
#             course=Courses.objects.get(id=course_id)
#             subject.course_id=course
#             subject.save()

#             messages.success(request,"Successfully Edited Subject")
#             return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
#         except:
#             messages.error(request,"Failed to Edit Subject")
#             return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


# def edit_course(request,course_id):
#     course=Courses.objects.get(id=course_id)
#     return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})

# def edit_course_save(request):
#     if request.method!="POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
#         course_id=request.POST.get("course_id")
#         course_name=request.POST.get("course")

#         try:
#             course=Courses.objects.get(id=course_id)
#             course.course_name=course_name
#             course.save()
#             messages.success(request,"Successfully Edited Course")
#             return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
#         except:
#             messages.error(request,"Failed to Edit Course")
#             return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))


# def manage_session(request):
#     sess_ug= SessionYearModel.object.filter(session_for = "ug")
#     sess_pg= SessionYearModel.object.filter(session_for = "pg")
#     return render(request,"hod_template/manage_session_template.html" , {"sess_ug":sess_ug,"sess_pg":sess_pg})

# def add_session_save(request):
#     if request.method!="POST":
#         return HttpResponseRedirect(reverse("manage_session"))
#     else:
#         session_year_for=request.POST.get("session_year_for")
#         session_start_year=request.POST.get("session_start")
#         session_end_year=request.POST.get("session_end")

#         try:
#             sessionyear=SessionYearModel(session_for = session_year_for,session_start_year=session_start_year,session_end_year=session_end_year)
#             sessionyear.save()
#             messages.success(request, "Successfully Added Session")
#             return HttpResponseRedirect(reverse("manage_session"))
#         except Exception as e:
#             messages.error(request, "Failed to Add Sessions")
#             return HttpResponseRedirect(reverse("manage_session"))

# @csrf_exempt
# def check_email_exist(request):
#     email=request.POST.get("email")
#     user_obj=CustomUser.objects.filter(email=email).exists()
#     if user_obj:
#         return HttpResponse(True)
#     else:
#         return HttpResponse(False)

# @csrf_exempt
# def check_username_exist(request):
#     username=request.POST.get("username")
#     user_obj=CustomUser.objects.filter(username=username).exists()
#     if user_obj:
#         return HttpResponse(True)
#     else:
#         return HttpResponse(False)

# @csrf_exempt
# def check_mobile_exist(request):
#     mobile=request.POST.get("mobile")
#     user_obj=Students.objects.filter(mobile=mobile).exists()
#     if user_obj:
#         return HttpResponse(True)
#     else:
#         return HttpResponse(False)


# @csrf_exempt
# def check_aaddhar_exist(request):
#     aaddhar=request.POST.get("aaddhar")
#     user_obj=Students.objects.filter(aaddhar=aaddhar).exists()
#     if user_obj:
#         return HttpResponse(True)
#     else:
#         return HttpResponse(False)

# def staff_feedback_message(request):
#     feedbacks=FeedBackStaffs.objects.all()
#     return render(request,"hod_template/staff_feedback_template.html",{"feedbacks":feedbacks})

# def student_feedback_message(request):
#     feedbacks=FeedBackStudent.objects.all()
#     return render(request,"hod_template/student_feedback_template.html",{"feedbacks":feedbacks})

# @csrf_exempt
# def student_feedback_message_replied(request):
#     feedback_id=request.POST.get("id")
#     feedback_message=request.POST.get("message")

#     try:
#         feedback=FeedBackStudent.objects.get(id=feedback_id)
#         feedback.feedback_reply=feedback_message
#         feedback.save()
#         return HttpResponse("True")
#     except:
#         return HttpResponse("False")

# @csrf_exempt
# def staff_feedback_message_replied(request):
#     feedback_id=request.POST.get("id")
#     feedback_message=request.POST.get("message")

#     try:
#         feedback=FeedBackStaffs.objects.get(id=feedback_id)
#         feedback.feedback_reply=feedback_message
#         feedback.save()
#         return HttpResponse("True")
#     except:
#         return HttpResponse("False")

# def staff_leave_view(request):
#     leaves=LeaveReportStaff.objects.all()
#     return render(request,"hod_template/staff_leave_view.html",{"leaves":leaves})

# def student_leave_view(request):
#     leaves=LeaveReportStudent.objects.all()
#     return render(request,"hod_template/student_leave_view.html",{"leaves":leaves})

# def student_approve_leave(request,leave_id):
#     leave=LeaveReportStudent.objects.get(id=leave_id)
#     leave.leave_status=1
#     leave.save()
#     return HttpResponseRedirect(reverse("student_leave_view"))

# def student_disapprove_leave(request,leave_id):
#     leave=LeaveReportStudent.objects.get(id=leave_id)
#     leave.leave_status=2
#     leave.save()
#     return HttpResponseRedirect(reverse("student_leave_view"))


# def staff_approve_leave(request,leave_id):
#     leave=LeaveReportStaff.objects.get(id=leave_id)
#     leave.leave_status=1
#     leave.save()
#     return HttpResponseRedirect(reverse("staff_leave_view"))

# def staff_disapprove_leave(request,leave_id):
#     leave=LeaveReportStaff.objects.get(id=leave_id)
#     leave.leave_status=2
#     leave.save()
#     return HttpResponseRedirect(reverse("staff_leave_view"))

# def admin_view_attendance(request):
#     subjects=Subjects.objects.all()
#     session_year_id=SessionYearModel.object.all()
#     return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

# @csrf_exempt
# def admin_get_attendance_dates(request):
#     subject=request.POST.get("subject")
#     session_year_id=request.POST.get("session_year_id")
#     subject_obj=Subjects.objects.get(id=subject)
#     session_year_obj=SessionYearModel.object.get(id=session_year_id)
#     attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
#     attendance_obj=[]
#     for attendance_single in attendance:
#         data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
#         attendance_obj.append(data)

#     return JsonResponse(json.dumps(attendance_obj),safe=False)


# @csrf_exempt
# def admin_get_attendance_student(request):
#     attendance_date=request.POST.get("attendance_date")
#     attendance=Attendance.objects.get(id=attendance_date)

#     attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
#     list_data=[]

#     for student in attendance_data:
#         data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
#         list_data.append(data_small)
#     return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

# def admin_profile(request):
#     user=CustomUser.objects.get(id=request.user.id)
#     return render(request,"hod_template/admin_profile.html",{"user":user})

# def admin_profile_save(request):
#     if request.method !="POST":
#         return HttpResponseRedirect(reverse("admin_profile"))
#     else:
#         first_name=request.POST.get("first_name")
#         last_name=request.POST.get("last_name")
#         password=request.POST.get("password")
#         try:
#             customuser=CustomUser.objects.get(id=request.user.id)
#             customuser.first_name=first_name
#             customuser.last_name=last_name
#             # if password!=None and password!="":
#             #     customuser.set_password(password)
#             customuser.save()
#             messages.success(request, "Successfully Updated Profile")
#             return HttpResponseRedirect(reverse("admin_profile"))
#         except:
#             messages.error(request, "Failed to Update Profile")
#             return HttpResponseRedirect(reverse("admin_profile"))

# def add_students_result(request):
#     session_year = SessionYearModel.object.all().order_by('-id')
#     subject = Subjects.objects.all().order_by('-id')
#     branch = Courses.objects.all().order_by('-id')
#     context={
#         'session_year':session_year,
#         'subject':subject,
#         'branch':branch
#     }
#     return render(request,"hod_template/add_students_result.html",context)

# def save_students_result(request):
#     if request.method!="POST":
#         return HttpResponseRedirect(reverse("add_students_result"))
#     else:
#         roll_number=request.POST.get("roll_number")
#         student_obj = CustomUser.objects.get(username=roll_number)
#         student_id = student_obj.id
        
#         student = Students.objects.get(admin_id=student_id)
#         session_year=student.session_year_id_id
#         branch=student.course_id_id
#         dob = student.dob
#         semester=request.POST.get("semester")
#         subject_name=request.POST.get("subject_name")
#         total_mark=request.POST.get("total_mark")
#         secured_mark=request.POST.get("secured_mark")
#         prac_total_mark=request.POST.get("prac_total_mark")
#         prac_secured_mark=request.POST.get("prac_secured_mark")
#         is_pass=request.POST.get("is_pass")
#         print(student_id,session_year,branch)
#         # try:
#         student_result = StudentResult(roll_number = roll_number,session_year = session_year,branch = branch,semester=semester,subject_name =subject_name,total_mark=total_mark,secured_mark=secured_mark,prac_total_mark=prac_total_mark,prac_secured_mark=prac_secured_mark,is_pass = is_pass,dob = dob)
#         student_result.save()
#         messages.success(request, " Result Added Successfully")
#         return HttpResponseRedirect(reverse("add_students_result"))
#         # except Exception as e:
#     messages.error(request, "Failed to Add Result {}")
#     return HttpResponseRedirect(reverse("add_students_result"))

# @csrf_exempt
# def check_rollNumber_exist(request):
#     roll_no=request.POST.get("roll_number")
#     user_obj=CustomUser.objects.filter(username=roll_no).exists()

#     if user_obj:
     
#         return HttpResponse(True)
#     else:
#         return HttpResponse(False)

# @csrf_exempt
# def fetch_rollNumber(request):
#     roll_number=request.POST.get("roll_number")
#     fetch_data = CustomUser.objects.get(username__exact=roll_number)
#     list_data={"name":fetch_data.first_name+" "+fetch_data.last_name,"id":fetch_data.id}
#     return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)
# def view_neet_students(request):
#     neet_students = NeetApply.objects.all().order_by('-id')
#     return render(request,"hod_template/view_neet_students.html",{"neet_students":neet_students})
# def delete_neet_student(request,neet_id):
#     neet=NeetApply.objects.get(id=neet_id).delete()
#     return HttpResponseRedirect(reverse("view_neet_students"))