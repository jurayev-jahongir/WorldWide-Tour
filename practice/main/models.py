from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Categories(models.Model):
    name = models.CharField(max_length=200, verbose_name='Названия категорие')
    slug = models.SlugField(verbose_name='ключ слова')
    dateCreate = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Дата создания')
    dateUpdate = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class TourIncluded(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(unique=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата созданиея' )
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Услуга в туре'
        verbose_name_plural = 'Услуги в туре'

    def __str__(self):
        return self.name


class TourLocation(models.Model):
    country = models.CharField(max_length=200, verbose_name='Страна')
    city = models.CharField(max_length=200, verbose_name='Город')
    slug = models.SlugField(unique=True, verbose_name='URL-ключ')
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(upload_to='media', verbose_name='Фото', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Статус')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Локация тура '
        verbose_name_plural = 'Локации туров'

    def __str__(self):
        return f'{self.city}, {self.country}'


class Tours(models.Model):
    name = models.CharField(max_length=200, verbose_name='Названия Тура')
    slug = models.SlugField(verbose_name='Ключ слова')
    category = models.ForeignKey(Categories, models.CASCADE, related_name='tours', verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    locations = models.ManyToManyField(TourLocation, blank=True, related_name='tours', verbose_name='Локации')
    included = models.ManyToManyField(TourIncluded, blank=True, verbose_name='Входит в стоимость')
    price = models.CharField(max_length=200, blank=True, verbose_name='Стоимость')
    free = models.PositiveIntegerField(verbose_name='Количество оставшихся мест', blank=True, default=0)
    is_popular = models.BooleanField(blank=True, null=True, verbose_name='Популярный')
    dateCreate = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Дата добовления')
    dateUpdate = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Дата изменения')


    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    def __str__(self):
        return self.name


class TourSchedule(models.Model):
    tour = models.ForeignKey(Tours, models.CASCADE, related_name='schedule')
    start_date = models.DateField(verbose_name='Начала тура')
    end_date = models.DateField(verbose_name='Конец тура')
    start_time = models.TimeField(verbose_name='Начало времени тура')
    end_time = models.TimeField(verbose_name='Конец времени тура')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available_places = models.PositiveIntegerField(verbose_name='Доступные места')
    dateCreate = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Дата добовления')
    dateUpdate = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Расписания тура'
        verbose_name_plural = 'Расписании туров'

    def __str__(self):
        return self.tour.name
    @property
    def duration(self):
        return (self.end_date - self.start_date).days


class TourImage(models.Model):
    tour = models.ForeignKey(Tours, models.CASCADE, related_name='image', verbose_name='Тур')
    img = models.ImageField(upload_to='tours', verbose_name='Фото')
    description = models.TextField(verbose_name='Описание')
    is_main = models.BooleanField(default=False, verbose_name='Главный фото')
    dateCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок фото')

    class Meta:
        verbose_name = 'Фото тура'
        verbose_name_plural = 'Фото туров'

    def __str__(self):
        return f"{self.tour.name} - {self.img.name}"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидания'),
        ('confirmed', 'Потверждено'),
        ('cancelled', 'Отменен'),
        ('completed', 'Завершено'),
    )
    user = models.ForeignKey(User, models.CASCADE, related_name='bookings', verbose_name='Пользователя')
    tour = models.ForeignKey(Tours, models.CASCADE, related_name='bookings', verbose_name='Тоур')
    schedule = models.ForeignKey(TourSchedule, models.CASCADE, related_name='bookings', verbose_name='Расписания')
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    number_of_people = models.PositiveIntegerField(default=1, verbose_name='Количество людей')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    comment = models.TextField(blank=True, verbose_name='Коментарии')



    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    def __str__(self):
        return f'{self.user.username} - {self.tour.name}'


class Contacts(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название компании')
    phone = models.CharField(max_length=200, verbose_name='Телефон')
    email = models.CharField(max_length=200, verbose_name='Почта')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    telegram = models.CharField(max_length=50, verbose_name='Телеграм', blank=True)
    instagram = models.CharField(max_length=50, verbose_name='Интсаграм', blank=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Дата изменения ')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.name


class Clients(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client',
                                verbose_name='Пользователь')

    address = models.CharField(max_length=100, verbose_name='Адрес', blank=True)
    phone = models.CharField(max_length=25,  blank=True, verbose_name='Телефон')
    email = models.EmailField(max_length=50, blank=True, verbose_name='Почта')

    date_create = models.DateTimeField(auto_now_add=True,  verbose_name='Дата ')
    date_update = models.DateTimeField(auto_now=True, verbose_name='')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.user.get_full_name() or self.user.username

#То есть твоя текущая структура — хорошая база, но для полноценного проекта я бы добавил как минимум:
#TourImage — фотографии тура;
#Booking — бронирование;
#возможно TourLocation — страны/города;
#возможно TourIncluded — что входит в стоимость;
#возможно Review — отзывы.*/