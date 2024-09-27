from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from books.models import Book


# Add post using class based view
@method_decorator(login_required, name='dispatch')
class AddBookCreateView(CreateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('add_book')
    def form_valid(self, form):
        return super().form_valid(form)



# Editing post using class based view
@method_decorator(login_required, name='dispatch')
class EditBookView(UpdateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'add_Book.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('homepage')


@login_required
def delete_post(request, id):
    post = models.Book.objects.get(pk=id)
    post.delete()
    return redirect('homepage')


# Deleting post using class based view
@method_decorator(login_required, name='dispatch')
class DeleteBookView(DeleteView):
    model = models.Book
    template_name = 'delete_book.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'


class DetailBookView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'

    
    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data=self.request.POST)
        post = self.get_object()
        if review_form.is_valid():
            new_comment = review_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object 
        comments = post.comments.all()
        comment_form = forms.ReviewForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context
    

@login_required
def buy_book(request, id):
    book = get_object_or_404(Book, pk=id)
    if book.quantity > 0:
        book.quantity -= 1
        book.save()
        return redirect('detail_book', id=id)
    else:
        return render(request, 'book_detail.html', {'book': book, 'error': 'This car is out of stock'})

    