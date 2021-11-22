from django.db import models
# from django.contrib.auth.models import User
from users.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Word(models.Model):
    word = models.CharField(max_length=200, unique=True)
    trans = models.CharField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['word']

    def __str__(self):
        return self.word


class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    translator = models.CharField(max_length=200, null=True, blank=True)
    reciter_count = models.IntegerField(default=0)
    save_count = models.IntegerField(default=0)
    words_total = models.IntegerField(default=0)
    difficulty_degree = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class ReciterWord(models.Model):
    reciter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    word = models.ForeignKey(Word, on_delete=models.SET_NULL, null=True)
    mastery_degree = models.IntegerField(null=True)
    note = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class ReciterBook(models.Model):
    reciter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='book')
    unfamiliar_words = models.IntegerField(default=0)
    familiar_words = models.IntegerField(default=0)
    reading_progress = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class BookWord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    word = models.ForeignKey(Word, on_delete=models.SET_NULL, null=True)
    note = models.TextField(null=True, blank=True)
    word_frequency = models.IntegerField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'word')


class Sentence(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    word = models.ForeignKey(Word, on_delete=models.SET_NULL, null=True)
    sentence = models.CharField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sentence






