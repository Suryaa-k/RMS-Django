from django.contrib import admin
from .models import Restaurant, MenuItem


class MenuItemInline(admin.TabularInline):
    """Show menu items inline on the Restaurant admin page."""
    model  = MenuItem
    extra  = 1
    fields = ("name", "dish_type", "category", "price", "is_available")


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display  = ("name", "rating", "address", "created_at")
    list_filter   = ("rating",)
    search_fields = ("name", "address")
    ordering      = ("-created_at",)
    inlines       = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display  = ("name", "restaurant", "dish_type", "category", "price", "is_available")
    list_filter   = ("dish_type", "category", "is_available")
    search_fields = ("name", "restaurant__name")
