from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from books.models import Book
from .forms import DepositForm
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal



@login_required
def deposit(request):
    user = request.user
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            latest_transaction = Transaction.objects.filter(user=user).last()
            current_balance = latest_transaction.remaining_balance if latest_transaction else 0
            new_balance = current_balance + amount

            request.session['remaining_balance'] = float(new_balance) 

            send_mail(
                'Deposit Successful',
                f'Dear {user.username},\n\nYour deposit of {amount} Taka was successful! Your new balance is {new_balance} Taka.\n\nThank you!',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, f'Deposit of {amount} Taka successful! Your new balance is {new_balance} Taka.')

            return redirect('transaction_report')
    else:
        form = DepositForm()
    return render(request, 'deposit.html', {'form': form})




@login_required
def borrow_book(request, book_id):
    user = request.user
    book = Book.objects.get(id=book_id)
    

    current_balance = Decimal(request.session.get('remaining_balance', 0.0))
    
    borrowing_price = book.borrowing_price

    if current_balance >= borrowing_price:
        new_balance = current_balance - borrowing_price
        request.session['remaining_balance'] = float(new_balance)  

        transaction = Transaction.objects.create(
            user=user,
            book=book,
            amount=-borrowing_price,
            remaining_balance=new_balance,
            transaction_type='borrow'
        )
        transaction.save()
        

        book.quantity -= 1
        book.save()

        send_mail(
            'Book Borrowed Successfully',
            f'Dear {user.username},\n\nYou have successfully borrowed "{book.title}". Your remaining balance is {new_balance} Taka.\n\nThank you!',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        messages.success(request, f'You have successfully borrowed "{book.title}". Your remaining balance is {new_balance} Taka.')
        
        
        return redirect('transaction_report')
    else:
        return render(request, 'error.html', {'message': "Insufficient balance to borrow this book."})




@login_required
def transaction_report(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')

    remaining_balance = float(request.session.get('remaining_balance', 0))

    return render(request, 'transaction_report.html', {
        'transactions': transactions, 
        'remaining_balance': remaining_balance
    })
