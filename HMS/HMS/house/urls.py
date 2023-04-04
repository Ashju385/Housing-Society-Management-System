from django.urls import path
from .views import ServiceListView, BookingListView, ServiceDetailView, CancelBookingView, homePage, loginPage, logoutUser, registerPage

app_name='house'

urlpatterns=[
    path('service_list/', ServiceListView, name='ServiceListView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('service/<catagory>', ServiceDetailView.as_view(), name='ServiceDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('', homePage, name='home'),
]