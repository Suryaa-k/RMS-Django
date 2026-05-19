from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Restaurant(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField()
    address     = models.CharField(max_length=500)
    rating      = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return f"{self.name} (Rating: {self.rating}/5)"

    def get_star_display(self):
        return "★" * self.rating + "☆" * (5 - self.rating)


class MenuItem(models.Model):
    """A single item on a restaurant's menu."""

    # ── Dish type (Veg / Non-Veg / Vegan) ──────────────────────────
    VEG     = "veg"
    NON_VEG = "non_veg"
    VEGAN   = "vegan"
    DISH_TYPE_CHOICES = [
        (VEG,     "Veg"),
        (NON_VEG, "Non-Veg"),
        (VEGAN,   "Vegan"),
    ]

    # ── Course category (Starter / Main / Dessert / Beverage) ───────
    STARTER  = "starter"
    MAIN     = "main"
    DESSERT  = "dessert"
    BEVERAGE = "beverage"
    CATEGORY_CHOICES = [
        (STARTER,  "Starter"),
        (MAIN,     "Main Course"),
        (DESSERT,  "Dessert"),
        (BEVERAGE, "Beverage"),
    ]

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menu_items",
    )
    name      = models.CharField(max_length=255, help_text="Name of the dish.")
    dish_type = models.CharField(
        max_length=10, choices=DISH_TYPE_CHOICES, default=VEG,
        help_text="Veg, Non-Veg, or Vegan."
    )
    category  = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES, default=MAIN,
        help_text="Course this dish belongs to."
    )
    price     = models.DecimalField(
        max_digits=8, decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price in ₹."
    )
    is_available = models.BooleanField(default=True, help_text="Currently on the menu?")
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "name"]
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return f"{self.name} — ₹{self.price} ({self.get_dish_type_display()})"
