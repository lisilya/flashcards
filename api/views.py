from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .serializers import CategorySerializer, FlashcardSerializer
from .models import Category, Flashcard
from bs4 import BeautifulSoup
import requests
import spacy
from django.db.models import F

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

    @action(detail=True, methods=['post'])
    def correct_answer(self, request, pk=None):
        flashcard = self.get_object()
        flashcard.correct_answers += 1
        flashcard.save()
        return Response({'status': 'correct answer counter incremented'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def incorrect_answer(self, request, pk=None):
        flashcard = self.get_object()
        flashcard.incorrect_answers += 1
        flashcard.save()
        return Response({'status': 'incorrect answer counter incremented'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def delete_flashcard(self, request, pk=None):
        flashcard = self.get_object()
        flashcard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@action(detail=False, methods=['post'])
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
                flashcard_data = {
                    'question': str(sent),
                    'answer': 'TBD',
                    'correct_answers': 0,
                    'incorrect_answers': 0,
                }
                serializer = FlashcardSerializer(data=flashcard_data) # type: ignore
                if serializer.is_valid():
                    serializer.save()
                flashcards.append(flashcard_data)
    return Response(flashcards)

@api_view(['GET'])
def getLessKnownFlashcards(request):
    flashcards = Flashcard.objects.annotate(knowledge_ratio=F('correct_answers') / (F('correct_answers') + F('incorrect_answers'))).order_by('knowledge_ratio')[:10]
    serializer = FlashcardSerializer(flashcards, many=True)
    return Response(serializer.data)