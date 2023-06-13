from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import FlashcardSerializer
from .models import Flashcard

class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

    @action(detail=True, methods=['post'])
    def correct_answer(self, request, pk=None):
        flashcard = self.get_object()
        flashcard.correct_answers += 1
        flashcard.save()
        return Response({'status': 'correct answer counter incremented'}, status=status.HTTP_200_OK)
    