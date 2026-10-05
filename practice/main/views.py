from django.shortcuts import render, get_object_or_404, redirect
from .models import TourIncluded, TourLocation, Tours, TourSchedule, TourImage, Categories, Booking, Contacts, Clients
from django.core.paginator import Paginator
from django.db.models.functions import Cast
from django.db.models import DecimalField
from .forms import ClientRegistrationForm
from django.contrib.auth import login, logout
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("main:home")
    else:
        form = AuthenticationForm(request)
    return render(request, 'main/login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.save()
                Clients.objects.create(
                    user=user,
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                )
            login(request, user)
            return redirect("main:home")
    else:
        form = ClientRegistrationForm()
    return render(request, 'main/register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("main:home")


def index(request):
    if request.user.is_authenticated:
        templates = 'main/index.html'
        tours = Tours.objects.all()
        popular_tours = Tours.objects.filter(is_popular=True)
        categories = Categories.objects.all()
        paginator = Paginator(tours, 4)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        contacts = Contacts.objects.all()

        context = {
            'tours': tours,
            'categories': categories,
            'page_obj': page_object,
            'popular_tours': popular_tours,
            'contacts': contacts,

        }
        return render(request, templates, context)
    else:
        return redirect("main:login")


def tours(request):
    if request.user.is_authenticated:
        category = request.GET.get('category', 'all')
        date = request.GET.get('date')
        city = request.GET.get('city')

        tours = Tours.objects.all()
        if category:
            if category != "all":
                tours = tours.filter(category__slug=category)
            else:
                tours = Tours.objects.all()
        if date:
            tours.filter(schedule__start_date=date)
        if city:
            tours.filter(locations__city=city)
        sort = request.GET.get('sort', 'popular')
        templates = 'main/tours.html'

        tours = tours.annotate(
            price_number=Cast("price", DecimalField(max_digits=10, decimal_places=2))
        )
        if sort == 'cheap':
            tours = tours.order_by('price_number')
        elif sort == 'expensive':
            tours = tours.order_by('-price_number')
        elif sort == 'new':
            tours = tours.order_by('-id')
        else:
            tours = tours.order_by('id')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
            tours = tours.filter(price_number__gt=min_price)
        if max_price:
            tours = tours.filter(price_number__lt=max_price)
        tour_type = request.GET.get('type')
        if tour_type:
            tours = tours.filter(category__slug=tour_type)
        people = request.GET.get('people')
        categories = Categories.objects.all()

        print("PEOPLE:", people)
        if people:
            people = int(people)
            tours = tours.filter(
                free__gte=people
            ).distinct()

        paginator = Paginator(tours, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        tours_count = tours.count()

        context = {

            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'sum': tours_count,
            'categories': categories,


        }
        return render(request, templates, context)
    else:
        return redirect("main:login")


def tour_detail(request, tour_slug):
    if request.user.is_authenticated:
        templates = 'main/tour_detail.html'
        tour = get_object_or_404(Tours, slug=tour_slug)
        locations = tour.locations.all()
        schedules = TourSchedule.objects.filter(tour=tour)
        contacts = Contacts.objects.all()
        category = tour.category.slug
        context = {
            'tour': tour,
            'locations': locations,
            'schedules': schedules,
            "contacts": contacts,
            'category': category,
        }
        return render(request, templates, context)
    else:
        return redirect("main:login")


def booking(request, tour_slug, schedule_id):
    if request.user.is_authenticated:
        tour = get_object_or_404(Tours, slug=tour_slug)
        schedule = get_object_or_404(TourSchedule, id=schedule_id, tour=tour)
        if request.method == 'POST':
            number = int(request.POST['number_of_people'])
            comment = request.POST['comment']
            price = number * int(tour.price)
            booking = Booking.objects.create(user=request.user, tour=tour, schedule=schedule, number_of_people=number,
                                             status='pending', total_price=price, comment=comment)
            schedule = TourSchedule.objects.get(id=schedule_id, tour=tour)
            free = schedule.available_places - number
            tour.free = free
            schedule.available_places = free
            tour.save()
            schedule.save()
            return redirect("main:booking", tour_slug=tour.slug, schedule_id=schedule.id)

        else:
            templates = 'main/booking.html'


            context = {
                'tour': tour,

            }
            return render(request, templates, context)
    else:
        return redirect("main: login")

# /                       → Главная
# /tours/                 → Все туры
# /tours/<slug>/          → Детальная страница тура
# /locations/             → Все направления
# /locations/<slug>/      → Конкретное направление
# /booking/<id>/          → Бронирование
#5. CTA «Получить консультацию»
#