from django.db import models
import datetime
from django.contrib.auth.models import User

from django.db.models import fields

# Create your models here.
class City_A(models.Model):
    city_id = models.CharField(max_length=5,primary_key=True)
    city_name = models.CharField(max_length=50)
    airport = models.TextField()
    class Meta:
        db_table = "city"
        managed = False
    def __str__(self):
        return self.city_name
        
#Destination
class City_B(models.Model):
    city_id = models.CharField(max_length=5,primary_key=True)
    city_name = models.CharField(max_length=50)
    airport = models.TextField()
    class Meta:
        db_table = "city"
        managed = False
    def __str__(self):
        return self.city_name
        
class City(models.Model):
    city_id = models.CharField(max_length=5,primary_key=True)
    city_name = models.CharField(max_length=50)
    airport = models.TextField()
    class Meta:
        db_table = "city"
        managed = False
    def __str__(self):
        return self.city_name

class Path(models.Model):
    path_id = models.CharField(max_length=5,primary_key=True)
    departure = models.CharField(max_length=5)
    destination = models.CharField(max_length=5)
    class Meta:
        db_table = "path"
        managed = False
    def __str__(self):
        return str(self.path_id)

class FlightClass(models.Model):
    flight_id = models.CharField(max_length=5,primary_key=True)
    seat_class = models.CharField(max_length=10)
    price = models.IntegerField()
    class Meta:
        db_table = "flight_class"
        unique_together = (("flight_id", "seat_class"),)
        managed = False
    def __str__(self):
        return str(self.flight_id)

class Flight(models.Model):
    flight_id = models.ForeignKey(FlightClass,on_delete=models.CASCADE, db_column='flight_id')
    airline = models.CharField(max_length=100)
    path_id = models.ForeignKey(Path,on_delete=models.CASCADE, db_column='path_id')
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.TimeField()
    arrival_date = models.DateTimeField(blank=True,null=True)
    departure_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        db_table = "flight"
        managed = False
    def __str__(self):
        return str(self.flight_id)

class Passenger(models.Model):
    id_no = models.CharField(max_length=20,primary_key=True) # id card/passport nunmber 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    ticket_id = models.CharField(max_length=10)
    class Meta:
        db_table = "passenger"
        managed = False
    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name} {self.email}"

class Payment(models.Model):
    card_no = models.CharField(max_length=20,primary_key=True)
    username = models.CharField(max_length=100)
    holder_name = models.CharField(max_length=100)
    ticket_id = models.CharField(max_length=10)
    class Meta:
        db_table = "payment"
        managed = False
    def __str__(self):
        return str(self.card_no)

class Ticket(models.Model):
    ticket_id = models.CharField(max_length=10,primary_key=True)
    flight_id = models.CharField(max_length=5)
    username = models.CharField(max_length=100)
    seat_class = models.CharField(max_length=10)
    total_amount = models.FloatField(null=True, blank=True)
    departure_date = models.DateField()
    booking_date = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=10)
    class Meta:
        db_table = "ticket"
        managed = False
    def __str__(self):
        return str(self.ticket_id)
