from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Service, Booking
from .forms import AvailabilityForm, CreateUserForm
from .booking_functions.availability import check_availability
from django.core.mail import  send_mail
from django.conf import settings
from django.core.mail import EmailMessage

# Create your views here.

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for' + user)

            return redirect('house:login')

    context = {'form': form}
    return render(request, 'sign_up.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('house:home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('house:home')


def homePage(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def ServiceListView(request):
    service_catagory_url_list = get_service_cat_url_list()
    context = {
        "service_list": service_catagory_url_list,
    }
    return render(request, 'service_list_view.html', context)


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class ServiceDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        catagory = self.kwargs.get('catagory', None)
        human_format_service_catagory = get_service_catagory_human_format(catagory)
        form = AvailabilityForm()
        if human_format_service_catagory is not None:
            context = {
                'service_catagory': human_format_service_catagory,
                'form': form,
            }
            return render(request, 'service_detail_view.html', context)
        else:
            return HttpResponse("Catagory does not exist")

    def post(self, request, *args, **kwargs):
        catagory = self.kwargs.get('catagory', None)
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

        available_services = get_available_services(catagory, data['check_in'], data['check_out'])
        if available_services is not None:
            booking = book_service(request, available_services[0], data['check_in'], data['check_out'])
            return render(request, 'success.html')
        else:
            return render(request, 'failur.html')


class CancelBookingView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('house:BookingListView')


def check_availability(service, check_in, check_out):
    avail_list = []
    booking_list = Booking.objects.filter(service=service)
    for booking in booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)


def book_service(request, service, check_in, check_out):
    booking = Booking.objects.create(
        user=request.user,
        service=service,
        check_in=check_in,
        check_out=check_out,
    )
    subject='Confirmed'
    msg='Your booking is Confirmed !! hehe'
    ee=EmailMessage(
        subject,
        msg,
        settings.EMAIL_HOST_USER,
        ['allaboutgaming2nt3@gmail.com'],
    )
    ee.send()
    booking.save()
    return booking


def get_available_services(catagory, check_in, check_out):
    service_list = Service.objects.filter(catagory=catagory)

    available_services = []

    for service in service_list:
        if check_availability(service, check_in, check_out):
            available_services.append(service)

    if len(available_services) > 0:
        return available_services
    else:
        return None


def get_service_cat_url_list():
    service = Service.objects.all()[0]
    service_catagories = dict(service.SERVICE_CATAGORIES)

    def get_service_catagory_human_format(catagory):
        service = Service.objects.all()[0]
        service_catagory = dict(service.SERVICE_CATAGORIES).get(catagory, None)
        return service_catagory

    service_cat_url_list = []

    for catagory in service_catagories:
        service_catagory = service_catagories.get(catagory)
        service_url = reverse('house:ServiceDetailView', kwargs={'catagory': catagory})

        service_cat_url_list.append((service_catagory, service_url))

    return service_cat_url_list


def get_service_catagory_human_format(catagory):
    service = Service.objects.all()[0]
    service_catagory = dict(service.SERVICE_CATAGORIES).get(catagory, None)
    return service_catagory
