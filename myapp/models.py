from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .managers import ItemManager
from django.utils import timezone

# Create your models here.

class Item(models.Model):

    class Meta:
        # Composite Key
        indexes = [
            models.Index(fields = ['added_by', 'item_price'])
        ]

    def __str__(self):
        return f"{self.item_name} : {self.item_price}"


    # For existing items
    def get_absolute_url(self):
        return reverse('myapp:index')

    # To delete and add some parameters
    def delete(self, using = None, keep_parents = False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


    item_name = models.CharField(max_length= 200, db_index=True)
    item_description = models.TextField()
    item_price = models.DecimalField(max_digits=14, decimal_places=2, db_index=True)
    item_image = models.URLField(max_length=500, default='https://cdn.vectorstock.com/i/500p/97/36/food-smile-logo-cartoon-food-lettering-vector-33389736.jpg')
    is_available = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    added_on = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False) # Soft delete flag

    deleted_at = models.DateTimeField(null=True, blank=True)  #Saves timestamp when deleted

    # item_image = models.CharField(max_length=500, default='https://cdn.vectorstock.com/i/500p/97/36/food-smile-logo-cartoon-food-lettering-vector-33389736.jpg')

    objects = ItemManager()
    all_objects = models.Manager()
    

class Category(models.Model):

    def __str__(self):
        return self.category_name

    category_name = models.CharField(max_length=200)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    added_on = models.DateField(auto_now=True)


def get_objects(request):

    item_list = Item.objects.only('item_name')

    for item in item_list:

        print(item.item_name)
