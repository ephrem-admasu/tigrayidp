from django.shortcuts import render, get_object_or_404, redirect
from .models import AidPackage, AidItem
from .forms import AidItemForm, AidPackageForm
from idp.models import FamilyMember, FamilyHead
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from idp.views import dashboard
from datetime import date, datetime, timedelta, timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from .priority import PriorityQueue

# Create your views here.

@login_required
def package_list(request):
    pkg = AidPackage.objects.all()
    pkg_form = AidPackageForm()

    return render(
        request,
        'aid/aidpackages.html',
        {
            'packages': pkg,
            'pkg_form': pkg_form
        }
    )

@login_required
def package_detail(request, id):
    pkg = get_object_or_404(AidPackage, id=id)
    aiditem_form = AidItemForm(initial={'aid_package': pkg})
    return render(
        request,
        'aid/aidpackage_detail.html',
        {
            'aidpackage_detail': pkg,
            'aiditem_form': aiditem_form
        }
    )  

@login_required
def add_aiditem(request, id):
    pkg = get_object_or_404(AidPackage, id=id)

    if request.method == 'POST':
        aiditem_form = AidItemForm(request.POST)
        print(aiditem_form)
        if aiditem_form.is_valid():
            obj = aiditem_form.save(commit=False)
            obj.save()
            # cd = aiditem_form.cleaned_data
            # aiditem = AidItem.objects.create(**cd)
            # aiditem.save()
            # print(cd)
            return HttpResponseRedirect(pkg.get_absolute_url())
        else:
            print(aiditem_form.errors)
    else:
        aiditem_form = AidItemForm()
    return render(
        request,
        'aid/aidpackage_detail.html',
        {
            'aidpackage_detail': pkg,
            'aiditem_form': aiditem_form
        }
    )

def get_aid_list(request, pkg):
    aidseekers_qs = FamilyHead.objects.filter(available=True)
    if not request.user.is_superuser:
        aidseekers_qs = aidseekers_qs.filter(address__subcity=redirect.user.stuff.work_place)
    aidpackage_list = []
    pq = PriorityQueue()
    if pkg.target_group == 'Family':
        # aidseekers_qs = FamilyHead.objects.filter(available=True)
        for p in aidseekers_qs:
            pq.push(p, p.family_priority())
    elif pkg.target_group == 'Children':
        # aidseekers_qs = FamilyHead.objects.filter(available=True)
        for p in aidseekers_qs:
            pq.push(p, p.children_priority())
    elif pkg.target_group == 'Pregnant or Lactating':
        # aidseekers_qs = FamilyHead.objects.filter(available=True)
        for p in aidseekers_qs:
            pq.push(p, p.lact_pregnant_priority())
    elif pkg.target_group == 'Elderly':
        # aidseekers_qs = FamilyHead.objects.filter(available=True)
        for p in aidseekers_qs:
            pq.push(p, p.elderly_priority())
    elif pkg.target_group == 'Disabled':
        # aidseekers_qs = FamilyHead.objects.filter(available=True)
        for p in aidseekers_qs:
            pq.push(p, p.disabled_priority())
    # elif pkg.target_group == 'Lactating':
    #     # aidseekers_qs = FamilyHead.objects.filter(available=True)
    #     for p in aidseekers_qs:
    #         pq.push(p, p.lactating_priority())
    for fh in range(int(pkg.quota)):
        # fh = pq.pop()
        # fh.aid_package = pkg 
        # fh.save()
        aidpackage_list.append(pq.pop())
    return aidpackage_list

@login_required
def publish_aidpackage(request, id):

    pkg = get_object_or_404(AidPackage, id=id)

    aidpackage_list = get_aid_list(request, pkg)
    return render(
        request, 
        'aid/publish.html',
        {
            'aid_list': aidpackage_list,
            'package': pkg
        }
    )

@login_required
def published_aidpackage(request, id):
    pkg = get_object_or_404(AidPackage, id=id)
    pkg.status = True 
    pkg.save()
    aidpackage_list = get_aid_list(request, pkg)
    for fh in aidpackage_list:
        
        fh.save()
        fh.aid_packages.add(pkg) 
    
    
    
    return render(
        request, 
        'aid/publish.html',
        {
            'aid_list': aidpackage_list,
            'package': pkg
        }
    )

class AidPackageDetailView(DetailView):
    context_object_name = 'aidpackage_detail'
    model = AidPackage
    template_name = 'aid/aidpackage_detail.html'

class AidPackageCreateView(CreateView):
    fields = ('package_name', 'target_group', 'quota', 'distribution_date')
    model = AidPackage
