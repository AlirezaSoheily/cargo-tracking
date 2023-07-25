from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='main'),
    path('car/', views.CarView.as_view(), name='car main'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('add_car/', views.CarCreateView.as_view(), name='add new car'),
    path('update_car/<int:pk>', views.CarUpdateView.as_view(), name='update car'),
    path('cars_list/', views.cars_list_view, name='cars list'),
    path('delete_car/<int:id>', views.car_delete_view, name='delete car'),

    path('add_service/', views.ServiceCreateView.as_view(), name='add service'),
    path('update_service/<int:pk>', views.ServiceUpdateView.as_view(), name='update service'),
    path('service_list/', views.services_list_view, name='service list'),
    path('delete_service/<int:id>', views.service_delete_view, name='delete service'),

    path('daily_report/', views.DailyReport.as_view(), name='daily report'),
    path('monthly_report/', views.MonthlyReport.as_view(), name='monthly report'),
    path('car_report/', views.CarReport.as_view(), name='car report'),
    path('contractor_report/', views.ContractorReport.as_view(), name='contractor report'),

]
