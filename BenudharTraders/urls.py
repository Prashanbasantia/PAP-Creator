"""BenudharTraders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main_app import admin_views ,user_views,login_views
from BenudharTraders import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login', login_views.login, name='login'),
    path('verify_login', login_views.verify_login, name='verify_login'),
    path('logout', login_views.logout, name='logout'),
    path('forget_password', login_views.forget_password, name='forget_password'),
    path('forget_password_otp_send',login_views.forget_password_otp_send,name="forget_password_otp_send"),
    path('forget_password_otp_verify',login_views.forget_password_otp_verify,name="forget_password_otp_verify"),
    path('set_new_password_save',login_views.set_new_password_save,name="set_new_password_save"),

    #All Admin_templete urls
    path('dashboard', admin_views.dashboard, name='dashboard'),
    path('admin_profile',admin_views.admin_profile,name='admin_profile'),
    path('admin_change_name',admin_views.admin_change_name,name='admin_change_name'),
    path('admin_change_mobile',admin_views.admin_change_mobile,name='admin_change_mobile'),
    path('password_verify_admin_change_mobile',admin_views.password_verify_admin_change_mobile,name="password_verify_admin_change_mobile"),
    path('admin_change_password',admin_views.admin_change_password,name="admin_change_password"),
    path('admin_change_profile_image',admin_views.admin_change_profile_image,name='admin_change_profile_image'),
    path('add_product', admin_views.add_product, name='add_product'),
    path('save_product', admin_views.save_product, name='save_product'),
    path('view_product', admin_views.view_product, name='view_product'),
    path('edit_product/<str:prod_id>', admin_views.edit_product, name='edit_product'),
    path('update_product', admin_views.update_product, name='update_product'),

    path('add_category', admin_views.add_category, name='add_category'),
    path('save_category', admin_views.save_category, name='save_category'),
    
   
    path('add_customer', admin_views.add_customer, name='add_customer'),
    path('otp_verify', admin_views.otp_verify, name='otp_verify'),
    path('save_customer', admin_views.save_customer, name='save_customer'),
    path('view_customer', admin_views.view_customer, name='view_customer'),
    path('view_inac_customer', admin_views.view_inac_customer, name='view_inac_customer'),
    path('edit_customer/<str:cust_id>', admin_views.edit_customer, name='edit_customer'),
    path('update_customer', admin_views.update_customer, name='update_customer'),
    path('delete_customer/<str:cust_id>', admin_views.delete_customer, name='delete_customer'),
    path('inventory', admin_views.inventory, name='inventory'),
    path('add_item', admin_views.add_item, name='add_item'),
    path('save_item', admin_views.save_item, name='save_item'),

    path('receipt', admin_views.receipt, name='receipt'),
    path('save_receipt', admin_views.save_receipt, name='save_receipt'),
    path('transaction', admin_views.transaction, name='transaction'),
    path('customer_transaction/<str:cust_id>', admin_views.cust_tran, name='cust_tran'),
    path('resend_user_otp',admin_views.resend_user_otp,name="resend_user_otp"),
    

    # path('admin_view_transaction', admin_views.view_transaction, name='view_transaction'),
    # # path('admin_generate_paymentcode', admin_views.generate_paymentcode, 
    # #     name='generate_paymentcode'),
    # # path('admin_profile', admin_views.profile, name='profile'),
    # path('admin_update_profile', admin_views.updateProfile, name='updateProfile'),

    #all user_template url
    path('', user_views.home, name='home'),
    path('user_receipt', user_views.user_receipt, name='user_receipt'),
    path('img', admin_views.img, name='img'),
    path('img_upload', admin_views.img_upload, name='img_upload'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

