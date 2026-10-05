from django.contrib import admin
from .models import Categories, Tours, TourSchedule, TourImage, Booking, TourLocation, TourIncluded, Contacts, Clients


@admin.register(Tours)
class ToursAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'dateUpdate', 'dateCreate')
    prepopulated_fields = {
        'slug': ('name',),
    }
    list_filter = ('name',)


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'dateCreate', 'dateUpdate')
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(TourSchedule)
class TourScheduleAdmin(admin.ModelAdmin):
    list_display = ('tour', 'start_time', 'end_time', 'dateCreate', 'dateUpdate')


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ('tour', 'img', 'tour', 'dateCreate')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'booking_date')


@admin.register(TourLocation)
class TourLocationAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'is_active', 'date_create', 'date_update')
    list_filter = ('country', 'is_active')
    search_fields = ('country', 'city')
    prepopulated_fields = {
        'slug': ('city', ),
    }
    readonly_fields = ('date_create', 'date_update',)


@admin.register(TourIncluded)
class TourIncludedAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'date_create', 'date_update')


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram', 'date_create', 'date_update')


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_create', 'date_update')