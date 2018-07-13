from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid # Required for unique book instances
from datetime import date

# Create your models here.

# Genres
class Genre(models.Model):
    # Fields
    genreType = models.CharField(max_length=200, help_text="Enter genre")

    def __str__(self):
        return self.genreType
    
# Books
class Book(models.Model):
    # Fields
    title = models.CharField(max_length=200, help_text="Enter book title")
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=300, help_text="Summary of the book")
    isbn = models.CharField("ISBN", max_length=20, help_text="A long row of digits")
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey("Language", on_delete=models.SET_NULL, null=True)

    # Methods
    def display_genre(self):
        # Creates a string for the Genre. This is required to display Genre in admin.
        return ", ".join([ genre.genreType for genre in self.genre.all()[:3] ] )
        display_genre.short_description = "Genre"

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id) ] )
    
    def __str__(self):
        return self.title

# Authors
class Author(models.Model):
    # Fields
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # Metadata
    class Meta:
        ordering = ["last_name","first_name"]

    # Methods
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id) ] )
    
    def __str__(self):
        return '{0}, {1}'.format(self.last_name,self.first_name)

# Languages
class Language(models.Model):
    # Fields
    language = models.CharField(max_length=200, help_text="Which language is the book written in?")
    
    def __str__(self):
        return self.language

# BookInstance - loaned or not
class BookInstance(models.Model):
    # Fields
    imprint = models.CharField(max_length=20, help_text="Who is the publisher?")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Book loan status field definition
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text="Book availability")

    # Metadata
    class Meta:
        ordering = ["due_back"]
        permissions = ( ("can_mark_returned", "Set book as returned"), )
    
    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)

    # Keeps track of if a user has borrowed a book (or more)
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False