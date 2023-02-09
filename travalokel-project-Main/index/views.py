from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.db.models import Max
from django.db import transaction
from .models import *
import json
import re
from django.db import connection
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'index.html')

def booking(request):
    return render(request,'booking.html')

def bookingflight(request):
    return render(request, 'ticket_info.html')

def my_booking(request):
    tickets = list(Ticket.objects.filter(username=request.user.username).order_by('-ticket_id').values('ticket_id','flight_id','departure_date',
                                                                                            'seat_class','total_amount','booking_date','status'))
    data=dict()
    data['tickets'] = tickets
    return render(request, 'my_booking.html', data)

def Addpassenger(request):
    if request.method == 'POST':
        if Passenger.objects.count() != 0:
            id_no_max = Passenger.objects.aggregate(Max('id_no'))['id_no__max']
            id_no_temp = [re.findall(r'(\w+?)(\d+)', id_no_max)[0]][0]
            next_id_no = id_no_temp[0] + str(int(id_no_temp[1])+1)
        else:
            next_id_no = "7201"
        fname           = request.POST['First_name']
        lname           = request.POST['Last_name']
        email           = request.POST['email']
        phone           = request.POST['phonenumber']

        flight_id       =   request.POST['flight_id']
        seat_class      =   request.POST['seat_class']
        total_amount    =   request.POST['total_amount']
        username        =   request.POST['username']
        booking_date    =   request.POST['booking_date']
        departure_date  =   request.POST['departure_date']
        ticket = createticket(flight_id,seat_class,total_amount,username,booking_date,departure_date)
        
        passenger = Passenger.objects.create(
                id_no=next_id_no,
                first_name=fname, 
                last_name=lname, 
                email=email,
                phone_no=phone,
                ticket_id=ticket)
        ticket_id = ticket.ticket_id
        try:passenger.save()
            
        except: redirect('/')
    return render(request,'payment.html',{'ticket_id':ticket_id,'total_amount':total_amount})

def createticket(flight_id,seat_class,total_amount,username,booking_date,departure_date):  
    if Ticket.objects.count() != 0:
        ticket_id_max = Ticket.objects.aggregate(Max('ticket_id'))['ticket_id__max']
        next_ticket_id = ticket_id_max[0:6] + str(int(ticket_id_max[6:10])+1)
    else:
        next_ticket_id = "TICKET1001"

    ticket_id = next_ticket_id
    booking_date = reFormatDateYYYYMMDDV2(booking_date)
    
    ticket = Ticket.objects.create(
            ticket_id=ticket_id,
            flight_id=flight_id,
            seat_class=seat_class,
            total_amount=total_amount,
            username =username,
            booking_date=booking_date,
            departure_date=departure_date,
            status = 'PENDING'                    
            )
    ticket.save()
    return ticket

def payment(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        card_no = request.POST.get('card_no')
        username = request.POST.get('username')
        holder_name = request.POST.get('card_name')
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            ticket.status = 'COMPLETED'
            ticket.save()

            payment = Payment.objects.create(
                card_no = card_no,
                username = username,
                holder_name = holder_name,
                ticket_id = ticket_id
            )
            payment.save()


            return render(request,'completedpayment.html',{
                'ticket_id': ticket_id
        })
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Method must be post.")

@csrf_exempt    
def TicketDelete(request):
    if request.method == 'POST':
        ticket_id = request.POST["ticket_id"]
        data = dict()
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        if ticket:
            Passenger.objects.filter(ticket_id=ticket_id).delete()
            Payment.objects.filter(ticket_id=ticket_id).delete()
            ticket.delete()
            data['message'] = "Ticket Deleted!"
        else:
            data['error'] = "Error!"
    return redirect('/mybooking')

class CityList(View):
    def get(self,request):
        cities = list(City.objects.values('city_name'))
        data = dict()
        data['cities'] = cities
        return JsonResponse(data)

class PathList(View):
    def get(self,request):
        paths = list(Path.objects.all().values())
        data = dict()
        data['paths'] = paths
        
        return JsonResponse(data)

class PathDetail(View):
    def get(self, request, id):
        path = list(Path.objects.select_related("city").filter(path_id=id).values('path_id','departure__city_name','destination__city_name','departure__airport','destination__airport'))
        path_detail = list(Flight.objects.select_related("flight_id").filter(path_id=id).values('flight_id','airline','departure_time','arrival_time','path_id__departure','path_id__destination','flight_id__seat_class'))
        data = dict()
        data['path'] = path[0]
        data['path_detail'] = path_detail

        return JsonResponse(data)
        
class ClassList(View):
    def get(self, request):
        seat_classes = list(FlightClass.objects.all().values())
        data = dict()
        data['seat_classes'] = seat_classes
        return JsonResponse(data)

class FlightList(View):
    def get(self, request, start, goal, date, seat_type):
        path_id     = Path.objects.filter(departure=start,destination=goal).values('path_id')[0]['path_id']
        paths       = list(Path.objects.filter(departure=start,destination=goal).values())
        cities = list(City.objects.filter(city_id=start).values())
        cities2 = list(City.objects.filter(city_id=goal).values())
        flights     = Flight.objects.all().select_related('flight_id','path_id').filter(path_id=path_id,departure_date=date,flight_id__seat_class=seat_type).values('flight_id','airline','path_id','departure_time','arrival_time','departure_date','duration','arrival_date','path_id__departure','path_id__destination','flight_id__seat_class', 'flight_id__price')
        data = dict()
        data['paths'] = paths[0]
        data['flights'] = flights
        data['cities'] = cities[0] 
        data['cities2'] = cities2[0]
        return render(request, 'ticket_list.html', data)

class FlightDetail(View):
    def get(self, request, id):
        flight = list(Flight.objects.filter(flight_id=id).values('flight_id','airline','path_id','departure_time','arrival_time','duration','arrival_date', 'departure_date'))
        flight_detail = list(FlightClass.objects.select_related("flight_id").filter(flight_id=id).values('flight_id','seat_class','price'))
        paths = list(Path.objects.filter(path_id=Flight.objects.filter(flight_id=id).values('path_id')[0]["path_id"]).values())
        data = dict()
        data['flight'] = flight[0]
        data['flight_detail'] = flight_detail[0]
        data['paths'] = paths[0]
        return JsonResponse(data)

class TicketReport(View):
    def get(self, request, pk):
        ticket_id = pk
        ticket = list(Ticket.objects.filter(ticket_id=ticket_id).values('ticket_id', 'flight_id', 'seat_class', 'status', 'total_amount', 'username', 'booking_date', 'departure_date'))
        passenger = list(Passenger.objects.filter(ticket_id=ticket_id).order_by('id_no').values("id_no","ticket_id","first_name","last_name","phone_no","email"))
        flight_id = ticket[0]['flight_id']
        flight_detail = list(Flight.objects.select_related("flight_id","path_id").filter(flight_id=flight_id).values(
                                                            'flight_id','airline', 'path_id__departure', 'path_id__destination', 'arrival_date', 'arrival_time', 'departure_date', 'departure_time', 'duration', 'flight_id', 'path_id', 'path_id_id'))
        departure_code = flight_detail[0]['path_id__departure']
        destination_code = flight_detail[0]['path_id__destination']
        departure = list(City_A.objects.filter(city_id=departure_code).values('city_id','city_name','airport'))
        destination = list(City_B.objects.filter(city_id=destination_code).values('city_id','city_name','airport'))
        data = dict()
        data['ticket'] = ticket[0]
        data['passenger'] = passenger
        data['flight_detail'] = flight_detail[0]
        data['departure'] = departure[0]
        data['destination'] = destination[0]
        #return JsonResponse(data)
        return render(request, 'report.html', data)

class PrintTicket(View):
    def post(self, request):
        idTicket = request.POST["ticket_id"]
        ticket_detail= list(Ticket.objects.filter(ticket_id=idTicket).values('ticket_id','flight_id','username','seat_class'))
        flight_id = ticket_detail[0]['flight_id']
        flight_detail= list(Flight.objects.select_related("flight_id","path_id").filter(flight_id=flight_id).values('airline', 'path_id__departure', 'path_id__destination','arrival_time','departure_time'))
        city_from = City.objects.filter(city_id=flight_detail[0]['path_id__departure']).values('city_name')
        city_to = City.objects.filter(city_id=flight_detail[0]['path_id__destination']).values('city_name')

        data=dict()
        data['ticket_detail']=ticket_detail[0]
        data['flight_detail']=flight_detail[0]
        data['city_from'] = city_from[0]
        data['city_to'] = city_to[0]
        return render(request, 'printTicket.html', data )
        #return JsonResponse(data)


def reFormatDateMMDDYYYY(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[8:10] + "-" + ddmmyyyy[5:7] + "-" + ddmmyyyy[:4]

def reFormatDateYYYYMMDD(yyyymmdd):
    if (yyyymmdd == ''):
            return ''
    return yyyymmdd[6:10] + "-" + yyyymmdd[3:5] + "-" + yyyymmdd[:2]

def reFormatDateYYYYMMDDV2(yyyymmdd):
    if (yyyymmdd == ''):
        return ''
    return yyyymmdd[:4] + "-" + yyyymmdd[5:7] + "-" + yyyymmdd[8:10]

def reFormatNumber(str):
        if (str == ''):
            return ''
        return str.replace(",", "")