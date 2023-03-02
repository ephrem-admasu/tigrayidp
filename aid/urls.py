from django.urls import path
from . import views


app_name = 'aid'

urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('aidpackages/<int:id>/', views.package_detail, name='aidpackage_detail'),
    path('aidpackages/<int:id>/additem', views.add_aiditem, name='add_aiditem'),
    path('aidpackages/create/', views.AidPackageCreateView.as_view(), name='create_package'),  
    path('aidpackages/publish/<int:id>/', views.publish_aidpackage, name='publish'),
    path('aidpackages/published/<int:id>/', views.published_aidpackage, name='published'),
]