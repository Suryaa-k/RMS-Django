from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # ── Restaurant URLs ─────────────────────────────────────────────
    path("",                    views.restaurant_list,   name="restaurant_list"),
    path("<int:pk>/",           views.restaurant_detail, name="restaurant_detail"),
    path("new/",                views.restaurant_create, name="restaurant_create"),

    # ── Menu Item URLs (nested under a restaurant) ──────────────────
    path("<int:restaurant_pk>/menu/add/",                        views.menu_item_create, name="menu_item_create"),
    path("<int:restaurant_pk>/menu/<int:item_pk>/edit/",         views.menu_item_edit,   name="menu_item_edit"),
    path("<int:restaurant_pk>/menu/<int:item_pk>/delete/",       views.menu_item_delete, name="menu_item_delete"),
]
