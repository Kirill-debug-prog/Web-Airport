from django.db import models
from django.utils import timezone

class Airlines(models.Model):
    airline_name = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'airport.Airlines'
        verbose_name_plural = 'Airlines'

    def __str__(self):
        return self.airline_name


class ArrivalSchedule(models.Model):
    flight_number = models.CharField(max_length=10)
    route = models.CharField(max_length=15, default='')  # Указываем значение по умолчанию
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    transport_model = models.CharField(max_length=15)
    days_week = models.DateField(null=True, blank=True)
    airline_id = models.ForeignKey('Airlines', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('arrival_time',)


class DepartureSchedule(models.Model):
    flight_number = models.CharField(max_length=10)
    route = models.CharField(max_length=15)
    airline = models.ForeignKey(Airlines, on_delete=models.CASCADE)
    departure_date = models.DateField()
    departure_time = models.DateTimeField(unique=True)
    transport_model = models.CharField(max_length=15)
    days_week = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'airport.DepartureSchedule'


class Discount(models.Model):
    category = models.CharField(max_length=10)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()

    class Meta:
        db_table = 'airport.Discount'


class Flight(models.Model):
    flight_number = models.CharField(max_length=10, primary_key=True)
    airline = models.ForeignKey(Airlines, on_delete=models.CASCADE)
    transport_type = models.CharField(max_length=8)
    transport_model = models.CharField(max_length=15)
    departure_date = models.DateField()
    departure_time = models.TimeField(unique=True)
    arrival_date = models.DateField()
    arrival_time = models.TimeField(unique=True)
    departure_location = models.CharField(max_length=20)
    arrival_location = models.CharField(max_length=20)
    flight_status = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        db_table = 'airport.Flight'


class Notification(models.Model):
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE)
    send_date = models.DateField()
    send_time = models.TimeField()
    notification_text = models.TextField()

    class Meta:
        db_table = 'airport.Notification'


class Passenger(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=10)
    middle_name = models.CharField(max_length=15, null=True, blank=True)
    contact_info = models.CharField(max_length=12, unique=True)
    passport_details = models.CharField(max_length=10, unique=True)
    booking = models.CharField(max_length=20, unique=True, null=True, blank=True)


    class Meta:
        db_table = 'airport.Passenger'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Report(models.Model):
    report_type = models.CharField(max_length=10)
    report_period = models.TextField()
    creation_date = models.DateField()
    creation_time = models.TimeField()
    report_content = models.TextField()

    class Meta:
        db_table = 'airport.Report'


from django.db import models

class Reviews(models.Model):
    date_of_revocation = models.DateField(default=timezone.now)
    review_text = models.TextField()
    photo = models.ImageField(upload_to='reviews/', null=True, blank=True)
    name = models.CharField(max_length=100, default='Аноним')

    class Meta:
        db_table = 'airport.Reviews'



class Role(models.Model):
    role_name = models.CharField(max_length=25, unique=True)

    class Meta:
        db_table = 'airport.Role'


class Ticket(models.Model):
    number_of_ticket = models.CharField(max_length=13, primary_key=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    flight_number = models.CharField(max_length=20) 
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'airport.Ticket'


class User(models.Model):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=20, unique=True)
    password_hash = models.CharField(max_length=14, unique=True)
    salt = models.CharField(max_length=15, unique=True)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=10)
    middle_name = models.CharField(max_length=15, null=True, blank=True)
    registration_date = models.DateField()
    last_date_of_authorization = models.DateField(null=True, blank=True)
    last_date_of_deauthorization = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'airport.User'


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'airport.UserRole'


