from django.shortcuts import render, get_object_or_404, redirect
from .models import FamilyHead, FamilyMember
from .forms import FamilyHeadForm, FamilyMemberForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .views import dashboard
from datetime import date, datetime, timedelta, timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# _ID_NO_CONST_ = 624971806

Kebeles = [
    'Amora', 'Debre Genet', 'Hayelom', 'Hidase',
    'Tsinat Woyane'
]
WOREDA = {
    'Adi Haqi': [
        'Amora', 'Debre Genet', 'Hayelom', 'Hidase', 'Tsinat Woyane'
    ],
    'Ayder': [
        'Adiha', 'Ginbot 20', 'Maryam Dihan', 'Marta', 'Sertse'
    ],
    'Hadinet': [
        'Asmelash', 'Aynalem', 'Debri', 'Hidase', 'Metkel', 'Simret', 'Werie'
    ],
    'Hawelti': [
        'Adi Shumdhein', 'Hayelom', 'Hidas', 'Mommona', 'Selam'
    ],
    'Kedamay Woyane': [
        'Harya', 'Selam', 'Walta', 'Zeslasie'
    ],
    'Quiha': [
        'Abreha', 'Asmelash', 'May Tsedo', 'Shibta'
    ],
    'Semien': [
        'Dedebit', 'Endustry', 'Meles', 'Mesfin', 'Yekatit'
    ]
}

# Create your views here.
def home(request):
    return render(
        request,
        'idp/home.html'
    )

@login_required
def add_head(request):
    if request.method == 'POST':
        head_form = FamilyHeadForm(request.POST, request.FILES)
        if head_form.is_valid():
            head = head_form.save(commit=False)
            head.available = True
            head.created_by = request.user 
            head.total_hhs = head.male_hhs + head.female_hhs

            if head.idp_site != 'In Community':
                head.is_idp = True

            head.save()
            messages.success(request, 'Family head successfully created.')


            return HttpResponseRedirect(reverse('idp:dashboard'))
        else:
            print(head_form.errors)
    else:
        head_form = FamilyHeadForm()
    return render(request, 'idp/create_head.html', {'head_form': head_form})

@login_required
def add_member(request, id):
    idp = get_object_or_404(FamilyHead, id=id)
    if request.method == 'POST':
        member_form = FamilyMemberForm(request.POST, request.FILES)

        if member_form.is_valid():
            obj = member_form.save(commit=False)
            obj.created_by = request.user
            obj.family_head = idp
            obj.available = True
            obj.save()
            messages.success(request, 'Family member successfully created.')

            return HttpResponseRedirect(reverse('idp:detail', args=(idp.id,)))
        else:
            print(member_form.errors)
    else:
        member_form = FamilyHeadForm()
    return render(request, 'idp/create_member.html', {'member_form': member_form, 'idp': idp})

@login_required
def head_list(request):

    idps_ = FamilyHead.objects.filter(available=True)
    if not request.user.is_superuser:
        idps_ = idps_.filter(address__subcity=request.user.stuff.work_place)
    paginator = Paginator(idps_, 40)
    page = request.GET.get('page')
    try:
        idps = paginator.page(page)
    except PageNotAnInteger:
        idps = paginator.page(1)
    except EmptyPage:
        idps = paginator.page(paginator.num_pages)
    head_form = FamilyHeadForm()
    return render(
        request,
        'idp/partials/_idp_list.html',
        {   
            'page': page,
            'idps': idps, 
            'head_form': head_form
        }
    )



@login_required
def head_detail(request, id):
    idp = get_object_or_404(FamilyHead, id=id)
    members = FamilyMember.objects.filter(family_head=idp)
    member_form = FamilyMemberForm(initial={'available': True, 'family_head': idp, 'created_by': request.user})

    return render(
        request, 
        'idp/detail.html',
        {
            'idp': idp,
            'members': members,
            'member_form': member_form
        }
    )

@login_required
def dashboard(request):
    idps_ = FamilyHead.objects.filter(available=True)
    # for idp in idps_:
    #     idp.id_no = str(_ID_NO_CONST_ + idp.id)
    #     idp.save()
    if not request.user.is_superuser:
        idps_ = idps_.filter(address__subcity=request.user.stuff.work_place)
    paginator = Paginator(idps_, 40)
    page = request.GET.get('page')
    try:
        idps = paginator.page(page)
    except PageNotAnInteger:
        idps = paginator.page(1)
    except EmptyPage:
        idps = paginator.page(paginator.num_pages)
    head_form = FamilyHeadForm()
    return render(
        request,
        'idp/dashboard.html',
        {   
            'page': page,
            'idps': idps, 
            'head_form': head_form
        }
    )


    # idps = FamilyHead.objects.filter(available=True)
    # if not request.user.is_superuser:
    #     idps = FamilyHead.objects.filter(address__subcity=request.user.stuff.work_place)
    # # qts = AidQuota.objects.all()
    
    # return render(request,
    #             'idp/dashboard.html',
    #             {
    #                 'idps': idps,
    #                 # 'quotas': qts
    #             }
    #         )

@login_required
def search(request):
    if request.GET:
        search_term = request.GET['search_term']
        search_results = FamilyHead.objects.filter(
           Q(full_name__icontains=search_term) |
           Q(phone_no__icontains=search_term)
        )
        context = {
            'search_term': search_term,
            'results': search_results
        }
        return render(request, 'idp/search.html', context)
    else:
        return redirect('idp:dashboard')

@login_required
def children_list(request):
    qs = FamilyMember.objects.filter(available=True, age__lte = 5)

    return render(
        request,
        'idp/children.html',
        {'children': qs}
    )

@login_required
def lactating_list(request):
    qs_m = FamilyMember.objects.filter(available=True, plw=True)
    qs_h = FamilyHead.objects.filter(available=True, plw=True)

    return render(
        request,
        'idp/preg_lact_list.html',
        {
            'lactating_mem': qs_m,
            'lactating_head': qs_h,
            'count': qs_m.count
        }
    )


@login_required
def disabled_list(request):
    qs_m = FamilyMember.objects.filter(available=True, is_disabled=True)
    qs_h = FamilyHead.objects.filter(available=True, is_disabled=True)

    return render(
        request,
        'idp/disabled.html',
        {
            'disabled_mem': qs_m,
            'disabled_head': qs_h,
            'count': qs_m.count
        }
    )

@login_required
def old_list(request):
    qs_mem = FamilyMember.objects.filter(available = True, age__gte = 60)
    qs_head = FamilyHead.objects.filter(available = True, age__gte = 60)

    return render(
        request,
        'idp/old_idp.html',
        {
            'old_mem': qs_mem,
            'old_head': qs_head,
            'count': qs_mem.count
        }
    )

@login_required
def check_dups(request):
    idps = FamilyHead.objects.all()
    dups = []
    i = 1
    for idp in idps:
        qs = FamilyHead.objects.filter(full_name__contains = idp.full_name)
        if qs.count() > 1 and qs not in dups:
            dups.append(qs) 
    total_dups = len(dups)
    return render(
        request,
        'idp/check_dups.html',
        {
            'dups': dups,
            'total_dups': total_dups
        }
    )


@login_required
def statistics(request):

    queryset = FamilyHead.objects.all()
    q_f = queryset.filter(sex='Female')
    q_m = queryset.filter(sex='Male')
    labels_sex = ['Male', 'Female']
    data_sex = [q_m.count(), q_f.count()]

    labels_kebele  = WOREDA['Adi Haqi']
    data_kebele = [queryset.filter(ckebele=l).count() for l in labels_kebele]

    return render(
        request, 
        'idp/statistics.html',
        {
            'labels_sex': labels_sex,
            'data_sex': data_sex,
            'labels_kebele': labels_kebele,
            'data_kebele': data_kebele
        }
    )


from django.http import HttpResponse
from .resources import FamilyHeadResources, ChildrenResources, LactPregnantResources, ElderlyResources, DuplicateResource

@login_required
def export_excel(request):
    head_resources = FamilyHeadResources()
    dataset = head_resources.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="family_heads.xls"'
    return response


@login_required
def export_children_excel(request):
    children_resources = ChildrenResources()
    dataset = children_resources.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="children_idps.xls"'
    return response

@login_required
def export_lact_pregnant_excel(request):
    qs = LactPregnantResources()
    dataset = qs.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="lactating_pregnant_idps.xls"'
    return response

@login_required
def export_duplicates_excel(request):
    qs = DuplicateResource()
    dataset = qs.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="idp_duplicates.xls"'
    return response

