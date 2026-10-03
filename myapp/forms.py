from django import forms
from .models import Item

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item

        fields = ['item_name', 'item_description', 'item_price', 'item_image']

        widgets = {
            'item_name': forms.TextInput(attrs={"placeholder": "e.g. Bugatti Chiron Super Sport 300+", "required": True}),
            'item_description': forms.TextInput(attrs={"placeholder": "e.g. Powered by an 8.0-liter quad-turbocharged W16 engine that produces 1,500 to 1,600 horsepower. It accelerates from 0 to 100 km/h in 2.4 seconds and reaches a top speed limited to 420–440 km/h. Bugatti limited total production to 500 units.", "required": True}),
            'item_price': forms.NumberInput(attrs={"placeholder": "e.g. 4500000", "required": True}),
            'item_image': forms.URLInput(attrs={"placeholder": "e.g. https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6IArSXTueDHX4YzNSH4zhElEYSgOaIOsfzBYTp8L0KfigRbIbyYp0f4I&s=10", "required": False}),
        }

    def clean_item_price(self):
        price = self.cleaned_data["item_price"]
        if price < 0:
            raise forms.ValidationError("Price must be positive")
        return price

    def clean(self):
        cleaned =  super().clean()
        name = cleaned.get("item_name")
        description = cleaned.get("item_description")

        if name and description and name.lower() in description.lower():
            self.add_error("item_description", "Description should add new info beyond name")

        return cleaned