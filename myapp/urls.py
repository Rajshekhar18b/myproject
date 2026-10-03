from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'myapp'

urlpatterns = [

    # URL pattern of API
    path('items-json/', views.item_list_json, name = 'item-list-json'),

    # URL pattern of API built with DRF
    path('items-api/', views.item_list_api, name = 'item-list-api'),
    path('item-detail/<int:pk>/', views.item_detail_api, name = 'item_detail_api'),

    # URL pattern of Django App

    # Function Based view 
    # path('index/', cache_page(60*10) (views.index), name = 'index'),   #[url-caching]
    path('index/', views.index, name = 'index'),
    path('<int:id>/', views.detail, name = 'detail'),
    path('add/', views.createItem, name = 'add'),
    # path('update/<int:id>/', views.updateItem, name = 'updateItem'),
    # path('delete/<int:id>/', views.deleteItem, name = 'deleteItem'),

    # Class based view
    # path('index/', views.IndexClassView.as_view(), name = 'index'),
    # path('<int:pk>/', views.DetailClassView.as_view(), name = 'detail'),
    # path('add/', views.CreateItemClassView.as_view(), name = 'add'),
    path('update/<int:pk>/', views.UpdateItemClassView.as_view(), name = 'updateItem'),
    path('delete/<int:pk>/', views.DeleteItemClassView.as_view(), name = 'deleteItem'),
]