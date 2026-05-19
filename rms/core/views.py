from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Restaurant, MenuItem
from .forms  import RestaurantForm, MenuItemForm


# ═══════════════════════════════════════════════════════════════════
#  RESTAURANT VIEWS
# ═══════════════════════════════════════════════════════════════════

def restaurant_list(request):
    """Display all restaurants."""
    restaurants = Restaurant.objects.all()
    return render(request, "core/restaurant_list.html", {"restaurants": restaurants})


def restaurant_detail(request, pk):
    """
    Display one restaurant + its full menu card.
    Menu items are grouped by category for easy reading.
    """
    restaurant = get_object_or_404(Restaurant, pk=pk)

    # Group available menu items by course category
    menu_items = restaurant.menu_items.filter(is_available=True)

    # Build ordered grouped dict: Starter → Main → Dessert → Beverage
    category_order = ["starter", "main", "dessert", "beverage"]
    grouped_menu = {}
    for cat_key in category_order:
        items = menu_items.filter(category=cat_key)
        if items.exists():
            grouped_menu[MenuItem.CATEGORY_CHOICES[[c[0] for c in MenuItem.CATEGORY_CHOICES].index(cat_key)][1]] = items

    return render(request, "core/restaurant_detail.html", {
        "restaurant":   restaurant,
        "grouped_menu": grouped_menu,
        "total_items":  menu_items.count(),
    })


def restaurant_create(request):
    """GET → blank form. POST → validate, save, redirect."""
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save()
            messages.success(request, f'"{restaurant.name}" was added successfully!')
            return redirect("core:restaurant_list")
    else:
        form = RestaurantForm()
    return render(request, "core/restaurant_form.html", {"form": form, "title": "Add New Restaurant"})


# ═══════════════════════════════════════════════════════════════════
#  MENU ITEM VIEWS
# ═══════════════════════════════════════════════════════════════════

def menu_item_create(request, restaurant_pk):
    """Add a new menu item to a specific restaurant."""
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)

    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant        # Link to parent restaurant
            item.save()
            messages.success(request, f'"{item.name}" added to the menu!')
            return redirect("core:restaurant_detail", pk=restaurant_pk)
    else:
        form = MenuItemForm()

    return render(request, "core/menu_item_form.html", {
        "form":       form,
        "restaurant": restaurant,
        "title":      f"Add Menu Item — {restaurant.name}",
        "action":     "Add",
    })


def menu_item_edit(request, restaurant_pk, item_pk):
    """Edit an existing menu item."""
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
    item       = get_object_or_404(MenuItem, pk=item_pk, restaurant=restaurant)

    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{item.name}" updated successfully!')
            return redirect("core:restaurant_detail", pk=restaurant_pk)
    else:
        form = MenuItemForm(instance=item)     # Pre-fill form with existing data

    return render(request, "core/menu_item_form.html", {
        "form":       form,
        "restaurant": restaurant,
        "item":       item,
        "title":      f"Edit — {item.name}",
        "action":     "Save Changes",
    })


def menu_item_delete(request, restaurant_pk, item_pk):
    """
    GET  → confirmation page.
    POST → delete item, redirect to restaurant detail.
    """
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
    item       = get_object_or_404(MenuItem, pk=item_pk, restaurant=restaurant)

    if request.method == "POST":
        item_name = item.name
        item.delete()
        messages.success(request, f'"{item_name}" removed from the menu.')
        return redirect("core:restaurant_detail", pk=restaurant_pk)

    return render(request, "core/menu_item_confirm_delete.html", {
        "restaurant": restaurant,
        "item":       item,
    })
