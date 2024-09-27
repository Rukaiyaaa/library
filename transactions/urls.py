from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.deposit, name='deposit'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('transaction_report/', views.transaction_report, name='transaction_report'),
]
