from django.db import models


class ItemManager(models.Manager):

    def cheap_items(self):

        return self.filter(item_price__lt = 30000)

    def expensive_items(self):

        return self.filter(item_price__gt = 50000)

    def search(self, keyword):

        return self.filter(item_name__icontains = keyword)

    def get_queryset(self):
    
            return super().get_queryset().filter(is_deleted = False)
    
    def deleted(self):
        return super().get_queryset().filter(is_deleted = True)


# Can also write these raw sql queries to fetch and act

# items = Item.objects.raw("SELECT * FROM myapp_item WHERE item_price > %s", [price_limit])


# items = Item.objects.raw("SELECT * FROM myapp_item")



    
