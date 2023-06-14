from django.db import models

class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
