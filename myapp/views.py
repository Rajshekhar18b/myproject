from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import logging
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .serializers import ItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

logger = logging.getLogger(__name__)

@api_view(['GET'])
def item_list_api(request):
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    


@api_view(['GET', 'POST'])
def item_detail_api(request, pk):
    if request.method == 'GET':
        items = Item.objects.get(pk = pk)
        serializer = ItemSerializer(items)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ItemSerializer(data = request.data)
    



def item_list_json(request):
    items = Item.objects.all().values("id", "item_name", "item_description", "item_price")
    return JsonResponse(list(items), safe=False)




# @login_required
# @cache_page(60*10)        #seconds [view caching]
# @vary_on_headers("User-Agent")
def index(request):

    logger.info("Fetching items from the database")

    # Get items from the database
    item_list = Item.objects.all().order_by('-id')

    logger.debug(f"Found {item_list.count()} items in total")

    # Pagination
    paginator = Paginator(item_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Creating context
    # If used pagination, instead of item_list, page_obj is passed as context
    context = {
        'page_obj': page_obj
    }

    # Passing the context object to the render method along with the template
    return render(request, "myapp/index.html", context)


'''
class IndexClassView(ListView):
    model = Item 
    template_name = "myapp/index.html"
    context_object_name = 'item_list'

    def get_queryset(self):
    
        return super().get_queryset().filter(is_deleted = False)

'''

def detail(request, id):

    logger.info(f"[{timezone.now().isoformat()}] ID {request.user.id} requested item list from {request.META.get('REMOTE_ADDR')}")
    logger.info(f"Fetching item with ID:{id}")

    try:

        item_list = get_object_or_404(Item, pk=id)
        item_list = Item.objects.get(id = id)

        logger.debug(f"Item found with name {item_list.item_name} pricing ${item_list.item_price}")

    except Exception as e:

        logger.error("Error fetching item %s: %s", id, e)
        raise

    context = {
        'item_list': item_list
    }
    return render(request, "myapp/detail.html", context)

    
'''

class DetailClassView(DetailView):
    model = Item
    template_name = "myapp/detail.html"
    context_object_name = 'item_list'

'''


def createItem(request):

    form = ItemForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('myapp:index')

    context = {
            'form': form
        }
    return render(request, 'myapp/item_form.html', context)


'''
class CreateItemClassView(CreateView):
    # By default, it looks for item_form.html template
    #  if app_name is food, it looks for food_form.html template for create.
    model = Item
    fields = ['item_name', 'item_description', 'item_price', 'item_image']

    def form_valid(self, form):
        form.instance.added_by = self.request.user 
        return super().form_valid(form)
'''


'''
def updateItem(request, id):
    item_list = Item.objects.get(id = id)
    form = ItemForm(request.POST or None, instance = item_list)
    if form.is_valid():
        form.save()
        return redirect('myapp:index')
    context = {
        'form': form
    }

    return render(request, 'myapp/item-form.html', context)
'''

class UpdateItemClassView(UpdateView):
    model = Item
    fields = ['item_name', 'item_description', 'item_price', 'item_image']
    template_name_suffix = '_update_form'

    # def get_queryset(self):
    #     return Item.objects.filter(added_by = self.request.user)

 
'''
def deleteItem(request, id):
    item = Item.objects.get(id = id)
    if request.method == 'POST':
        item.delete()
        return redirect('myapp:index')
    
    return render(request, 'myapp/item-delete.html')
'''

class DeleteItemClassView(DeleteView):
    model = Item
    success_url = reverse_lazy('myapp:index')




# Queryset methods:
'''
1. Item.objects.all()               
    -> To get all the items

2. Item.objects.get()               
    -> To get only one object
    Ex: Item.objects.get(item_name = 'Fries')

3. Item.objects.filter()            
    -> To get the filtered item objects (Filters item_price greater than 80) (__gt used for greater than and __lt for less than, if used nothing it compares for exact values)
    Ex: Item.objects.filter(item_price__gt = 80)

4. Item.objects.exclude()           
    -> To exculde the specific records with specific values 
    # (Excludes item_price greater than 80)
    Ex: Item.objects.exclude(item_price__gt = 80) 

5. Item.objects.values()            
    -> To get the object list of dictionaries. 
    # (Extracting only item_name and item_price)
    Ex: Item.objects.values('item_name', 'item_price')

6. Item.objects.first()             
    -> To get the first object
    Ex: Item.objects.first()

7. Item.objects.last()              
    -> To get the last object
    Ex: Item.objects.last()

8. Item.objects.all().order_by()    
    -> To get the items in order i.e. ASC or DESC, specified in order_by (- for descending and nothing for ascending)
    Ex: Item.objects.all().order_by('-item_name')

9. Item.objects.count()             
    -> To get the count of number of objects.
    Ex: Item.objects.count()

10. Item.objects.filter('condition').exists()     
    -> Gives boolean value True if certain conditions meet and record exists else False
    Ex:Item.objects.filter(item_price__gt = 100).exists()

11. Item.objects.filter('lookup condition like generalSearch')          
    -> Works like generalSearch and gives objects that contains word pizza in item_name here.
    Ex: Item.objects.filter(item_name__contains='Pizza')    -> ['case-sensitive']
    Ex: Item.objects.filter(item_name__icontains='Pizza')   -> ['case-insensitive']

    # exact and iexact looks for the specified word and must not contain any extra words.

12. Item.objects.filter('lookup condition like generalSearch')          
    -> Gives objects that has exact word pizza in item_name here ['case-sensitive']
    Ex: Item.objects.filter(item_name__exact='Pizza')

13. Item.objects.filter('lookup condition like generalSearch')          
    -> Gives objects that has exact word pizza in item_name here ['case-insensitive' but looks for complete full word must not contain extra words]
    Ex: Item.objects.filter(item_name__iexact='Pizza')

14. Item.objects.filter('range specify here')
    -> To get the items within specified price range
    Ex: Item.objects.filter(item_price__range=(50, 80))

15. Item.objects.filter('startswith condition')
    -> To get the items that startswith the given letter. ['case-sensitive']
    Ex: Item.objects.filter(item_name__startswith = 'P')

14. Item.objects.filter('endswith condition')
    -> To get the items that endswith the given letter. ['case-sensitive']
    Ex: Item.objects.filter(item_name__endswith = 'a')

15. Item.objects.filter('endswith condition')
    -> To get the records that are created in that year or date.
    Ex: Item.objects.filter(added_on__year='2026')
    Ex: Item.objects.filter(added_on__date='2026-08-03')

16. Combining Multiple Filters
    Ex: Item.objects.filter(item_price__gt=100).filter(item_name__icontains = 'chicken')

    
from django.db.models import Sum, Min, Max, Avg
      
17. Sum
    Ex: Item.objects.aggregate(Sum('item_price'))

18. Min
    Ex: Item.objects.aggregate(Min('item_price'))

19. Max
    Ex: Item.objects.aggregate(Max('item_price'))

20. Average
    Ex: Item.objects.aggregate(Avg('item_price'))

'''