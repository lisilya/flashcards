from django.shortcuts import render
from rest_framework import viewsets
from .serializers import FlashcardSerializer
from .models import Flashcard

class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = Flashcard.object.all()
    serializer_class = FlashcardSerializer