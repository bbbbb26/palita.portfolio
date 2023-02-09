"""travarokel_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from app_users import views
from index import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('users/', include('app_users.urls')),
    path('booking',views.booking),
    path("CreateTicket",views.createticket),
    path('payment',views.Addpassenger),
    path('completedpayment',views.payment),
    path('mybooking',views.my_booking, name='mybooking'),
    path('cancelticket', views.TicketDelete, name="cancelticket"),
    path('city/list',views.CityList.as_view()),
    path('flight/detail/<str:id>',views.FlightDetail.as_view(),name="flightDetail"),
    path('flight/list/<str:start>/<str:goal>/<str:date>/<str:seat_type>',views.FlightList.as_view(),name="FlightList"),
    path('flight/booking',views.bookingflight, name="bookpage"),
    path('ticket/report/<str:pk>', views.TicketReport.as_view(), name='ticket_report'),
    path('ticket/print', views.PrintTicket.as_view(), name="printTicket"),
]
#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns += path('__debug__/',include(debug_toolbar.urls)),
urlpatterns += staticfiles_urlpatterns()