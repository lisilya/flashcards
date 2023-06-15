from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlashcardViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'flashcards', FlashcardViewSet, basename='flashcard')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/flashcards/from-url/', FlashcardViewSet.as_view({'post': 'create_flashcards_from_url'})),
]
