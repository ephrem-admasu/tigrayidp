from django.urls import path
from . import views

app_name = 'idp'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<int:id>', views.head_detail, name="detail"),
    path('add_head/', views.add_head, name='add_head'),
    path('detail/<int:id>/add_member/', views.add_member, name='add_member'),
    path('children/', views.children_list, name='children_list'),
    path('preg_lact_list/', views.lactating_list, name='preg_lact_list'),
    path('disabled/', views.disabled_list, name='disabled_list'),
    path('old/', views.old_list, name='old_list'),
    path('search/', views.search, name='search'),
    path('check_duplicates/', views.check_dups, name='check_dups'),
    # path('view_duplicates/', views.view_duplicates, name='view_dups'),
    path('household_excel/', views.export_excel, name='heads_excel'),
    path('children_excel/', views.export_children_excel, name='children_excel'),
    path('lact_pregnant_excel/', views.export_lact_pregnant_excel, name='preg_lact_excel'),
    path('duplicates/', views.export_duplicates_excel, name='duplicates'),
    path('statistics/', views.statistics, name='statistics')
    # path('head_pdf/', views.get_head_pdf, name='head_pdf'),
]