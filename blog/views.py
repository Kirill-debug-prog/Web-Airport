from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from .models import UserRole, Role

from .forms import RegisterCashierForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login as auth_login
from .forms import RegisterCashierForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import User

import json






def index(request):
    return render(request, 'blog/index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Определите роль пользователя через группы
                user_groups = user.groups.all()
                if user_groups.filter(name='cashiers').exists():
                    return redirect('flights')  # Путь для кассира
                elif user_groups.filter(name='system_admin').exists():
                    return redirect('admin_home')  # Путь для системного администратора
                else:
                    messages.error(request, 'Неизвестная роль пользователя.')
                    return redirect('login')
                
            else:
                messages.error(request, 'Неправильный логин или пароль.')
        else:
            messages.error(request, 'Неправильный логин или пароль.')
    else:
        form = LoginForm()
    
    return render(request, 'blog/login.html', {'form': form})

def cashier_home(request):
    return render(request, 'blog/Cashier_page.html')

def admin_home(request):
    return render(request, 'blog/System_Administrator.html')

def login_redirect(request):
    if request.user.groups.filter(name='cashier').exists():
        return redirect('cashier_home')  # страница для кассира
    elif request.user.groups.filter(name='admin').exists():
        return redirect('admin_home')  # страница для админа
    else:
        return redirect('home')  # основная страница для всех
    
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

@csrf_exempt
def add_cashier(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            surname = data.get('surname')
            name = data.get('name')
            email = data.get('email')
            login = data.get('login')
            password = data.get('password')

            if not (surname and name and email and login and password):
                return JsonResponse({'success': False, 'message': 'Все поля обязательны.'}, status=400)

            # Создание нового пользователя (кассира)
            user = User.objects.create(
                username=login,
                password=make_password(password),
                first_name=name,
                last_name=surname,
                email=email
            )

            # Присоединение пользователя к группе
            group, created = Group.objects.get_or_create(name='cashiers')
            user.groups.add(group)

            return JsonResponse({
                'success': True,
                'cashier': {
                    'surname': surname,
                    'name': name,
                    'email': email
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Ошибка в формате данных.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False}, status=400)

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import JsonResponse

# Страница с вводом данных кассира
def cashier_info(request):
    return render(request, 'blog/Cashier_details.html')

# Обработка поиска кассира по фамилии
def search_cashier(request):
    if request.method == 'GET':
        last_name = request.GET.get('last_name', '').strip()  # Получаем фамилию из запроса

        # Ищем пользователей с заданной фамилией, которые находятся в группе "cashiers"
        cashiers_group = Group.objects.get(name='cashiers')
        cashiers = User.objects.filter(last_name=last_name, groups=cashiers_group)

        if cashiers.exists():
            cashier = cashiers.first()  # Предположим, что фамилия уникальна
            data = {
                'last_name': cashier.last_name,
                'first_name': cashier.first_name,
                'username': cashier.username,
                'email': cashier.email,
                'date_joined': cashier.date_joined.strftime('%Y-%m-%d'),
            }
        else:
            data = {'error': 'Кассир не найден'}

        return JsonResponse(data)
    
from django.shortcuts import render
from .models import Reviews

def reviews_view(request):
    reviews = Reviews.objects.all()
    return render(request, 'blog/Reviews.html', {'reviews': reviews})
  

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Reviews
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

@csrf_exempt
def add_review(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'Аноним')
        review_text = request.POST.get('review_text', '')

        if not review_text:
            return JsonResponse({'status': 'error', 'message': 'Отзыв не может быть пустым.'})

        # Создание нового отзыва
        review = Reviews.objects.create(
            name=name,
            review_text=review_text,
            date_of_revocation=timezone.now()
        )
        review.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Неверный запрос.'})


from django.http import JsonResponse
from .models import ArrivalSchedule, DepartureSchedule

def get_arrival_schedule(request):
    arrivals = ArrivalSchedule.objects.all()
    schedule_data = []

    for arrival in arrivals:
        schedule_data.append({
            'flight_number': arrival.flight_number,
            'route': arrival.route,
            'airline_id': arrival.airline_id.airline_name,
            'arrival_date': arrival.arrival_date.strftime('%Y-%m-%d'),
            'arrival_time': arrival.arrival_time.strftime('%H:%M'),
            'transport_model': arrival.transport_model,
        })
    
    return JsonResponse(schedule_data, safe=False)

def get_departure_schedule(request):
    departures = DepartureSchedule.objects.all()
    schedule_data = []

    for departure in departures:
        schedule_data.append({
            'flight_number': departure.flight_number,
            'route': departure.route,
            'airline_id': departure.airline.airline_name,
            'departure_date': departure.departure_date.strftime('%Y-%m-%d'),
            'departure_time': departure.departure_time.strftime('%H:%M'),
            'transport_model': departure.transport_model,
        })
    
    return JsonResponse(schedule_data, safe=False)

def schedule_view(request):
    return render(request, 'blog/Schedule.html')  

from django.shortcuts import render

def passenger_info(request):
    return render(request, 'blog\Passenger_page.html')

from django.shortcuts import render
from .models import Flight


from django.http import JsonResponse
from .models import Flight

def search_flights(request):
    # Извлечение параметров запроса
    arrival_airport = request.GET.get('arrival_airport')
    departure_date = request.GET.get('departure_date')

    # Проверка на полноту ввода
    if not arrival_airport or len(arrival_airport) < 3:
        return JsonResponse({'flights': []})  # Возвращаем пустой список, если ввод неполный

    # Фильтрация рейсов по параметрам
    flights = Flight.objects.filter(
        arrival_location__icontains=arrival_airport,
        departure_date=departure_date
    ).values(
        'departure_time', 'arrival_time', 'airline__airline_name', 'flight_number',
        'departure_location', 'arrival_location', 'price'
    )

    # Подготовка данных для возврата
    flights_list = list(flights)
    return JsonResponse({'flights': flights_list})

def flight_search_view(request):
    return render(request, 'blog/Flights.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Passenger, Ticket, Flight
import uuid  # Для генерации уникального номера билета

@csrf_exempt
def book_flight(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Проверяем, существует ли уже пассажир с таким же паспортом или контактной информацией
        passenger, created = Passenger.objects.get_or_create(
            contact_info=data['contact_info'],
            passport_details=data['passport_details'],
            defaults={
                'last_name': data['last_name'],
                'first_name': data['first_name'],
                'middle_name': data.get('middle_name'),
                'booking': data['booking']
            }
        )
        
        # Проверяем, существует ли рейс с данным номером рейса
        try:
            flight = Flight.objects.get(flight_number=data['flight_number'])
        except Flight.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Flight not found'}, status=404)
        
        # Генерируем уникальный номер билета
        ticket_number = str(uuid.uuid4().hex[:13].upper())
        
        # Создаем запись билета
        ticket = Ticket(
            number_of_ticket=ticket_number,
            passenger=passenger,
            flight=flight,
            price=data['price'],
            flight_number=data['flight_number'],
            discount=data['discount'],
            total_price=data['total_price']
        )
        ticket.save()
        
        return JsonResponse({'success': True, 'ticket_number': ticket_number})
    return JsonResponse({'success': False}, status=400)


from django.http import JsonResponse
from .models import Passenger, Ticket

def search_passenger(request):
    if request.method == "GET":
        last_name = request.GET.get('last_name', None)
        if last_name:
            try:
                passenger = Passenger.objects.get(last_name=last_name)
                ticket = Ticket.objects.get(passenger=passenger)

                # Возвращаем данные пассажира и билета
                data = {
                    'last_name': passenger.last_name,
                    'first_name': passenger.first_name,
                    'middle_name': passenger.middle_name,
                    'contact_info': passenger.contact_info,
                    'passport_details': passenger.passport_details,
                    'flight_number': ticket.flight_number,
                    'booking': passenger.booking,
                    'discount': str(ticket.discount),
                }
                return JsonResponse({'status': 'success', 'data': data})
            except Passenger.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Пассажир не найден'})
            except Ticket.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Билет не найден'})
        return JsonResponse({'status': 'error', 'message': 'Фамилия не указана'})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Passenger, Ticket

@csrf_exempt
@require_http_methods(['POST'])
def update_passenger(request):
    import json
    data = json.loads(request.body)
    
    last_name = data.get('last_name')
    passenger = get_object_or_404(Passenger, last_name=last_name)
    
    passenger.first_name = data.get('first_name')
    passenger.middle_name = data.get('middle_name')
    passenger.contact_info = data.get('contact_info')
    passenger.passport_details = data.get('passport_details')
    passenger.booking = data.get('booking')
    passenger.save()

    ticket = Ticket.objects.filter(passenger=passenger).first()
    if ticket:
        ticket.flight_number = data.get('flight_number')
        ticket.discount = data.get('discount')
        ticket.save()
    
    return JsonResponse({'status': 'success'})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Passenger, Ticket

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_passenger(request):
    import json
    last_name = request.GET.get('last_name')

    if not last_name:
        return JsonResponse({'status': 'error', 'message': 'Фамилия не указана'}, status=400)

    try:
        passenger = get_object_or_404(Passenger, last_name=last_name)
        
        # Удаление всех билетов, связанных с пассажиром
        Ticket.objects.filter(passenger=passenger).delete()
        
        # Удаление самого пассажира
        passenger.delete()
        
        return JsonResponse({'status': 'success'})
    except Passenger.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Пассажир не найден'}, status=404)
