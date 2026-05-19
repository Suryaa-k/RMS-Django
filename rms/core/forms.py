from django import forms
from .models import Restaurant, MenuItem


class RestaurantForm(forms.ModelForm):
    class Meta:
        model  = Restaurant
        fields = ["name", "description", "address", "rating"]
        labels = {
            "name": "Restaurant Name", "description": "Description",
            "address": "Address",      "rating": "Rating (1–5)",
        }
        widgets = {
            "name":        forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. The Golden Fork"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "address":     forms.TextInput(attrs={"class": "form-control"}),
            "rating":      forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is not None and not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


class MenuItemForm(forms.ModelForm):
    """Form for creating and editing a MenuItem."""

    class Meta:
        model  = MenuItem
        fields = ["name", "dish_type", "category", "price", "is_available"]
        labels = {
            "name":         "Item Name",
            "dish_type":    "Type",
            "category":     "Course",
            "price":        "Price (₹)",
            "is_available": "Available on menu?",
        }
        widgets = {
            "name":      forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Paneer Butter Masala"}),
            "dish_type": forms.Select(attrs={"class": "form-control"}),
            "category":  forms.Select(attrs={"class": "form-control"}),
            "price":     forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01", "placeholder": "0.00"}),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
