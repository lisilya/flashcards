from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import FlashcardSerializer
from .models import Flashcard
from bs4 import BeautifulSoup
import requests
import spacy

class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

    @action(detail=True, methods=['post'])
    def correct_answer(self, request, pk=None):
        flashcard = self.get_object()
        flashcard.correct_answers += 1
        flashcard.save()
        return Response({'status': 'correct answer counter incremented'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def delete_flashcard(self, request, pk=None):
        flashcard = self.get_object()
        flashcard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def create_flashcards_from_url(self, request):
    url = request.data.get('url')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    nlp = spacy.load('en_core_web_sm')
    flashcards = []
    for paragraph in paragraphs:
        doc = nlp(paragraph.text)
        for sent in doc.sents:
            if len(sent) > 1:
                flashcards.append({
                    'question': str(sent),
                    'answer': 'TBD',
                })
    return Response(flashcards)