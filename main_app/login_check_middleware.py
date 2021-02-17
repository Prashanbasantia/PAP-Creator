from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print("module",modulename)        
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "main_app.admin_views":
                    pass
                elif  modulename == "django.views.static"  or reverse('logout'):
                    pass
                else:
                    return HttpResponseRedirect(reverse("dashboard"))
            elif user.user_type == "2":
                if modulename == "main_app.user_views":
                    pass
                elif modulename == "django.views.static" or reverse('logout'):
                    pass
                else:
                    return HttpResponseRedirect(reverse("home"))
            else:
                return HttpResponseRedirect(reverse("login"))

        else:
            if modulename == "main_app.login_views" or  modulename == "main_app.user_views" or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("home"))