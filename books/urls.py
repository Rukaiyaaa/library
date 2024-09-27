from django.urls import path
from . import views

urlpatterns = [ 
    path('add/', views.AddBookCreateView.as_view(), name='add_book'),
    path('edit/<int:id>/', views.EditBookView.as_view(), name='edit_book'),
    path('delete/<int:id>/', views.DeleteBookView.as_view(), name='delete_book'),
    path('detail/<int:id>/', views.DetailBookView.as_view(), name='detail_book'),
    path('buy/<int:id>/', views.buy_book, name='buy_book'),
]