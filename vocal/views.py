
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import (generics, mixins)

from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .models import (Book, Topic, Word, ReciterWord, ReciterBook, BookWord)
from .serializers import (BookSerializer, WordSerializer, ReciterWordSerializer, ReciterBookSerializer,
                          BookWordSerializer)
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class BookList(generics.GenericAPIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin):
    # permission_classes = [
    #     # IsAuthenticatedOrReadOnly,
    #     # IsOwnerOrReadOnly,
    #     IsAuthenticated
    # ]
    # authentication_classes = (TokenAuthentication,)

    serializer_class = BookSerializer

    def get_queryset(self):
        topic = self.request.query_params.get('topic')
        if topic is not None:
            queryset = Book.objects.filter(topic=topic)
        else:
            queryset = Book.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BookDetail(generics.GenericAPIView,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)


class ReciterBookList(generics.GenericAPIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin):
    # permission_classes = [
    #     # IsAuthenticatedOrReadOnly,
    #     # IsOwnerOrReadOnly,
    #     IsAuthenticated
    # ]
    # authentication_classes = (TokenAuthentication,)

    serializer_class = ReciterBookSerializer

    def get_queryset(self):
        queryset = ReciterBook.objects.filter(reciter=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(reciter=self.request.user)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class ReciterBookDetail(generics.GenericAPIView,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):

    queryset = ReciterBook.objects.all()
    serializer_class = ReciterBookSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)


class ReciterWordList(generics.GenericAPIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin):
    # permission_classes = [
    #     # IsAuthenticatedOrReadOnly,
    #     # IsOwnerOrReadOnly,
    #     IsAuthenticated
    # ]
    # authentication_classes = (TokenAuthentication,)

    serializer_class = ReciterWordSerializer

    def get_queryset(self):
        mastery_degree = self.request.query_params.get('mastery_degree')
        book = self.request.query_params.get('book')

        if book is not None:
            bookwords_queryset = BookWord.objects.filter(book=book)
            words_id_list = [i.word for i in bookwords_queryset]

            queryset = ReciterWord.objects.filter(
                Q(reciter=self.request.user) & Q(word__in=words_id_list)
            )
        elif mastery_degree is not None:
            queryset = ReciterWord.objects.filter(
                Q(reciter=self.request.user) & Q(mastery_degree=mastery_degree)
            )
        else:
            queryset = ReciterWord.objects.filter(reciter=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BookWordList(generics.GenericAPIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin):
    # permission_classes = [
    #     # IsAuthenticatedOrReadOnly,
    #     # IsOwnerOrReadOnly,
    #     IsAuthenticated
    # ]
    # authentication_classes = (TokenAuthentication,)

    serializer_class = BookWordSerializer

    def get_queryset(self):
        book = self.request.query_params.get('book')
        queryset = BookWord.objects.filter(book=book)
        return queryset

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
