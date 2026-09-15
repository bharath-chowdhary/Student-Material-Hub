from django.db import models
from django.utils import timezone
from google import genai
import os
# Create your me
class Section(models.Model):
    name=models.CharField(max_length=30)
    batch=models.IntegerField()
    def __str__(self):
        return f"{self.name}[{self.batch}]"
class Subject(models.Model):
    name=models.CharField(max_length=30)
    section=models.ForeignKey(Section,on_delete=models.CASCADE,related_name='subjects')
    def __str__(self):
        return f"{self.name}[{self.section}]"
class Document(models.Model):
    name=models.CharField(max_length=30)
    file=models.FileField(upload_to='documents/')
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='materials')
    uploaded_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.name)

class Admin(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    section=models.CharField(max_length=40)
    def __str__(self):
        return self.name
class Ai:
    def __init__(self,quest,file):
        self.asked=quest
        self.path=file
    def process(self):
        gemini_api_key = os.environ.get("GEMINI_API_KEY", "").strip().strip("'\"")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not configured.")
        client = genai.Client(api_key=gemini_api_key)
        model = os.environ.get('GEMINI_MODEL', 'gemini-3.6-flash')
        role = self.tune()
        uploaded_file = client.files.upload(file=self.path)

        
        response=client.models.generate_content(
            model=model,
            contents=[
                role,
                uploaded_file,
                self.asked
            ]
        )

        return response.text
    def tune(self):
        
        mentor='''
        Read the following file and understand user's question/query/doubt properly as Teacher/mentor, your role would be as mentor and you have
        to answer the questions asked by students, use the words and sentences in the file for responses.
        Or extract the answer from file Itself only! not on othersources -- high Priority,
        Must follow => metion "<br>" html tag for next line and don't inclue "*" and "**" this symbols unless it is in file.
        if related answer not exist, then say : "Sorry, I could not found anything about that!"
        "Kindly restrict your responses to file-related queries only;
        casual messages or greetings are not required". Always recheck before providing response.
        '''
        return mentor