from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from books.models import Book
from .forms import DepositForm
from django.http import HttpResponse
from django.contrib import messages



@login_required
def deposit(request):
    user = request.user
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            # Get the latest balance from the last transaction or default to 0
            latest_transaction = Transaction.objects.filter(user=user).last()
            current_balance = latest_transaction.remaining_balance if latest_transaction else 0
            new_balance = current_balance + amount

            # Convert Decimal to float before storing in session
            request.session['remaining_balance'] = float(new_balance)  # Store balance as float

            messages.success(request, f'Deposit of {amount} Taka successful! Your new balance is {new_balance} Taka.')

            return redirect('transaction_report')
    else:
        form = DepositForm()
    return render(request, 'deposit.html', {'form': form})



from decimal import Decimal

@login_required
def borrow_book(request, book_id):
    user = request.user
    book = Book.objects.get(id=book_id)
    
    # Get the user's latest balance and convert to Decimal
    current_balance = Decimal(request.session.get('remaining_balance', 0.0))
    
    # Get the borrowing price as Decimal
    borrowing_price = book.borrowing_price

    if current_balance >= borrowing_price:
        # Deduct the book price from the user's balance
        new_balance = current_balance - borrowing_price
        request.session['remaining_balance'] = float(new_balance)  # Store balance as float
        
        # Create a new transaction for borrowing the book
        transaction = Transaction.objects.create(
            user=user,
            book=book,
            amount=-borrowing_price,
            remaining_balance=new_balance,
            transaction_type='borrow'
        )
        transaction.save()
        
        # Reduce the book quantity
        book.quantity -= 1
        book.save()

        messages.success(request, f'You have successfully borrowed "{book.title}". Your remaining balance is {new_balance} Taka.')
        
        
        return redirect('transaction_report')
    else:
        return render(request, 'error.html', {'message': "Insufficient balance to borrow this book."})




@login_required
def transaction_report(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')

    # Get the current balance from the session and convert to float
    remaining_balance = float(request.session.get('remaining_balance', 0))

    return render(request, 'transaction_report.html', {
        'transactions': transactions, 
        'remaining_balance': remaining_balance
    })
