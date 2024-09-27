from django.db import models

# Create your models here.
class BookCategory(models.Model):
    book_category = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)


    def __str__(self):
        return self.book_category