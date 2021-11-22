from django.contrib import admin

# Register your models here.
from .models import Book, Topic, Word, ReciterWord, ReciterBook, BookWord, Sentence


@admin.register(Book)
class BookModel(admin.ModelAdmin):
    list_filter = ('topic', 'name')
    list_display = ('name', 'topic', )


admin.site.register(Topic)
admin.site.register(Word)


@admin.register(ReciterWord)
class ReciterWordModel(admin.ModelAdmin):
    list_display = ('word', 'reciter')


@admin.register(BookWord)
class BookWordModel(admin.ModelAdmin):
    list_display = ('word', 'book')


@admin.register(ReciterBook)
class ReciterBookModel(admin.ModelAdmin):
    list_display = ('book', 'reciter')


admin.site.register(Sentence)
