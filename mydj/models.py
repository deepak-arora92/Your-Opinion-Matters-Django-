#author :Deepak
#date : 25-03-2016 
from django.db import models
class Question(models.Model):
    def __str__(self):
        return  self.question_text
    question_text = models.TextField()
    pub_date = models.DateTimeField('date published')

class Users(models.Model):
    user_id= models.AutoField(primary_key=True)
    userName = models.CharField(max_length=200)
    emailId = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    
class Options(models.Model):
    def __str__(self):
        return  self.option_desc
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_desc = models.CharField(max_length=60)
    votes = models.IntegerField(default=0)

class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
