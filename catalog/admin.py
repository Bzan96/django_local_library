from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language, Publisher

# Register your models here.
#admin.site.register(Book)
#admin.site.register(BookInstance)
#admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Language)

# Inline information about each book when viewing author
class BookItemsInline(admin.TabularInline):
    model = Book
    extra = 0

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name")
    fields = ["first_name", "last_name"]
    inlines = [BookItemsInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# Inline information about each book when viewing book
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_publisher", "display_genre")
    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "borrower", "due_back", "id")
    list_filter = ("status", "due_back")

    fieldsets= (
        (None, {
            "fields": ("book", "imprint", "id")
        } ),
        ("Availability", {
            "fields": ("status", "due_back", "borrower")
        } ),
    )