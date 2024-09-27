from django import forms
from .models import BookCategory

class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = BookCategory
        fields = '__all__'