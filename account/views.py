from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from idp.models import FamilyHead, FamilyMember
from django.contrib.auth import logout as django_logout


# def user_login(request):

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)

#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('dashboard'))
#             else:
#                 return HttpResponse('You account is not active.')
#         else:
#             return HttpResponse("Invalid login details supplied!")
#     else:
#         return render(request, 'account/login.html', {})


# @login_required
# def logout(request):
#     django_logout(request)
#     return  HttpResponseRedirect('/deck')

# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponse(reverse('idp:home'))


class ThanksPage(TemplateView):
    template_name = 'account/thanks.html'

# @login_required
# def dashboard(request):
#     idps = FamilyHead.objects.filter(available=True, address__subcity=request.user.stuff.work_place)
#     # qts = AidQuota.objects.all()
    
#     return render(request,
#                 'account/dashboard.html',
#                 {
#                     'idps': idps,
#                     # 'quotas': qts
#                 }
#             )
