from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('books', views.BookViewSet, basename='books')

urlpatterns = [
    # path('', include(router.urls)),
    path('books/', views.BookList.as_view(), name='books'),
    path('books/<str:pk>/', views.BookDetail.as_view(), name='book'),
    path('bookwords/', views.BookWordList.as_view(), name='bookwords'),

    path('reciterbooks/', views.ReciterBookList.as_view(), name='reciter-books'),
    path('reciterbooks/<str:pk>/', views.ReciterBookDetail.as_view(), name='reciter-book'),

    path('reciterwords/', views.ReciterWordList.as_view(), name='bookwords-user'),

]
