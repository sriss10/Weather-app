from django.urls import path
from weather import views

urlpatterns=[

    path('',views.index, name='home'),
    path('delete/<city_name>/', views.delete_city,name='delete_city'),
    path('delete_everything/', views.delete_everything, name='delete_everything')
]
