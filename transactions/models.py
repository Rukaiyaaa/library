from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from datetime import datetime

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now)
    transaction_type = models.CharField(max_length=20, choices=[('deposit', 'Deposit'), ('borrow', 'Borrow')])


