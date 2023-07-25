from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from .models import Car, CarService
from django.urls import reverse_lazy
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)


class Index(View):
    def get(self, request):
        return render(request, 'core/main.html')


def login_user(request):
    password = request.POST.get('password')
    if user := authenticate(username='abdollah', password=password):
        login(request, user)
        return render(request, 'core/main.html')
    else:
        return HttpResponse("رمز عبور اشتباه است")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('main'))


class CarView(View):
    def get(self, request):
        render(request, 'car/main.html')


class CarCreateView(CreateView):
    model = Car
    template_name = 'car/AddNewCar.html'
    fields = ['plaque', 'Contractor', 'car_type']
    success_url = reverse_lazy('add new car')


class ServiceCreateView(CreateView):
    model = CarService
    template_name = 'car/add service.html'
    fields = ['car', 'date', 'amount', 'loading', 'discharge', 'description']
    success_url = reverse_lazy('add service')


class CarUpdateView(UpdateView):
    model = Car
    template_name = 'car/AddNewCar.html'
    fields = ['plaque', 'Contractor', 'car_type']
    success_url = reverse_lazy('cars list')


class ServiceUpdateView(UpdateView):
    model = CarService
    template_name = 'car/add service.html'
    fields = ['car', 'date', 'amount', 'loading', 'discharge', 'description']
    success_url = reverse_lazy('service list')


def cars_list_view(request):
    contex = {'cars': Car.objects.all().order_by('-id')}
    return render(request, 'car/cars_list_view.html', contex)


def services_list_view(request):
    contex = {'services': CarService.objects.all().order_by('-id')}
    return render(request, 'car/services list.html', contex)


def car_delete_view(request, id):
    context = {}

    obj = get_object_or_404(Car, id=id)

    if request.method == "POST":
        obj.delete()

        return HttpResponseRedirect(reverse_lazy('cars list'))

    return render(request, "car/delete_view.html", context)


def service_delete_view(request, id):
    context = {}

    obj = get_object_or_404(CarService, id=id)

    if request.method == "POST":
        obj.delete()

        return HttpResponseRedirect(reverse_lazy('service list'))

    return render(request, "car/service delete.html", context)


class DailyReport(View):
    def get(self, request):
        return render(request, 'car/daily report form.html')

    def post(self, request):
        context = {'date': request.POST.get('date')}
        if request.POST.get('date'):
            date = request.POST.get('date').replace('/', '-')
            services = CarService.objects.filter(date=date)
            tak_total = 0
            dah_charkh_total = 0
            for service in services:
                if service.car.car_type == 'تک':
                    tak_total += service.amount
                elif service.car.car_type == 'ده چرخ':
                    dah_charkh_total += service.amount
            context['services'] = services
            context['tak_total'] = tak_total
            context['dah_charkh_total'] = dah_charkh_total
        else:
            return HttpResponse('در این تاریخ گزارشی یافت نشد!')
        return render(request, 'car/daily report.html', context)


class MonthlyReport(View):
    def get(self, request):
        return render(request, 'car/monthly report form.html')

    def post(self, request):
        context = {'date1': request.POST.get('date1'), 'date2': request.POST.get('date2')}
        if request.POST.get('date1') and request.POST.get('date2'):
            date1 = request.POST.get('date1').replace('/', '-')
            date2 = request.POST.get('date2').replace('/', '-')
            services = CarService.objects.filter(date__gte=date1, date__lte=date2)
            tak_total = 0
            dah_charkh_total = 0
            for service in services:
                if service.car.car_type == 'تک':
                    tak_total += service.amount
                elif service.car.car_type == 'ده چرخ':
                    dah_charkh_total += service.amount
            context['services'] = services
            context['tak_total'] = tak_total
            context['dah_charkh_total'] = dah_charkh_total
        else:
            return HttpResponse('لطفا تاریخ را به درستی وارد کنید!')
        return render(request, 'car/monthly report.html', context)


class CarReport(View):
    def get(self, request):
        return render(request, 'car/car report form.html')

    def post(self, request):
        context = {'date1': request.POST.get('date1'), 'date2': request.POST.get('date2')}
        if request.POST.get('date1') and request.POST.get('date2') and request.POST.get('plaque'):
            date1 = request.POST.get('date1').replace('/', '-')
            date2 = request.POST.get('date2').replace('/', '-')
            plaque = request.POST.get('plaque')
            services = CarService.objects.filter(car__plaque=plaque, date__gte=date1, date__lte=date2)
        else:
            return HttpResponse('لطفا همه مقادیر را به درستی وارد کنید!')
        total_services = 0
        for service in services:
            total_services += service.amount
        context['services'] = services
        context['total_services'] = total_services
        context['car'] = Car.objects.get(plaque=plaque)
        return render(request, 'car/car report.html', context)


class ContractorReport(View):
    def get(self, request):
        return render(request, 'car/contractor report form.html')

    def post(self, request):
        cars = {}
        context = {'date1': request.POST.get('date1'), 'date2': request.POST.get('date2')}
        if request.POST.get('date1') and request.POST.get('date2') and request.POST.get('contractor'):
            date1 = request.POST.get('date1').replace('/', '-')
            date2 = request.POST.get('date2').replace('/', '-')
            contractor = request.POST.get('contractor')
            contractor_cars = Car.objects.filter(Contractor=contractor)
            for car in contractor_cars:
                services = CarService.objects.filter(car=car, date__gte=date1, date__lte=date2)
                total = 0
                for service in services:
                    total += service.amount
                cars[car] = total
        else:
            return HttpResponse('لطفا همه مقادیر را به درستی وارد کنید!')

        context['cars'] = cars
        context['contractor'] = contractor
        context['date1'] = request.POST.get('date1')
        context['date2'] = request.POST.get('date2')
        return render(request, 'car/contractor report.html', context)
