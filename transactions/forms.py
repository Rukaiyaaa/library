from django import forms

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Deposit Amount")
