from django.urls import path
from . import views
urlpatterns=[
    # path('',views.index,name='index'),
    path('materials/',views.Materials,name='materials'),
    path('',views.Sections,name='sections'),
    path('register/', views.Register,name='register'),
    path('addmaterial/',views.Addmatrial,name='addmaterial'),
    path('addsubject/',views.Addsubject,name='addsubject')

]