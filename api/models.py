from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
