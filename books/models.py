from django.db import models
from genre.models import BookCategory
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.IntegerField(default=50)
    image = models.ImageField(upload_to='books/')
    borrowing_price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name='genre')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title 


class Review(models.Model):
    post = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Comments by {self.user}"