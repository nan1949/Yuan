import json
from rest_framework import serializers
from .models import Book, Word, ReciterWord, ReciterBook, BookWord
from django.db.models import Q



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class BookWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookWord
        fields = '__all__'


class ReciterWordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReciterWord
        fields = ('id', 'mastery_degree', 'word', '_word', 'note')

    _word = serializers.SerializerMethodField('get_word')
    # books = serializers.SerializerMethodField('get_books')

    def get_word(self, obj):
        return obj.word.word

    # def get_books(self, obj):
    #     books_queryset = BookWord.objects.filter(
    #         Q(word=obj.word)
    #     )
    #     return BookWordSerializer(books_queryset, many=True).data


class ReciterBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReciterBook
        fields = ['id', 'book', 'book_name',  'unfamiliar_words', 'familiar_words', 'reading_progress']
        extra_kwargs = {
            'unfamiliar_words': {
                'read_only': True
            },
            'familiar_words': {
                'read_only': True
            },
            'word': {
                'read_only': True
            }
        }

    book_name = serializers.SerializerMethodField('get_book_name')

    def get_book_name(self, obj):
        return obj.book.name

    def create(self, validated_data):
        bookwords_data = BookWord.objects.filter(book=validated_data.get('book'))
        reciter = validated_data.get('reciter')
        reciterwords_data = ReciterWord.objects.filter(reciter=reciter)
        bookwords = [bookword_data.word for bookword_data in bookwords_data]
        reciterwords = [reciterword_data.word for reciterword_data in reciterwords_data]

        for word in [word for word in bookwords if word not in reciterwords]:
            ReciterWord.objects.create(reciter=reciter,
                                       word=word,
                                       mastery_degree=0)

        reciterbook = ReciterBook.objects.create(**validated_data)
        return reciterbook

