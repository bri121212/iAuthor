from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)
    # profile_picture = models.ImageField()
    textbooks = models.TextField(blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    textbooks = models.TextField(blank=True) # concatenated string of textbook ids

    def __str__(self):
        return self.name

class Textbook(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    published_chapters = models.TextField(blank=True) # concatenated string of chapter ids
    unpublished_chapters = models.TextField(blank=True) # concatenated string of chapter ids

    def __str__(self):
        return self.name
    
class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    isPublished = models.BooleanField(default=False)
    elements = models.TextField(blank=True) # concatenated string of element ids
    skills = models.TextField(blank=True) # concatenated string of skill ids 

    def __str__(self):
        return self.textbook.name + " - " + self.name

# class Element(models.Model):
#     ELEMENT_TYPE = {
#         "paragraph": "Paragraph",
#         "note": "Note",
#         "example": "Example",
#         "subsection": "Subsection",
#         "image": "Image",
#         "video": "Video", 
#         "mcq": "MCQ",
#         "fib": "FIB",
#         "likert": "Likert",
#     }
#     id = models.AutoField(primary_key=True) 
#     element_type = models.CharField(max_length=16, choices=ELEMENT_TYPE)
#     chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
#     detail_id = models.IntegerField() # references the id of the specific content type

#     def __str__(self):
#         return self.chapter.textbook.name + " - " + self.chapter.name + " " + str(self.id) + " - " + self.element_type 
 
    

class Content(models.Model):
    # ELEMENT_TYPE = {
    #     "paragraph": "Paragraph",
    #     "note": "Note",
    #     "example": "Example",
    #     "subsection": "Subsection",
    #     "image": "Image",
    #     "video": "Video"
    # }
    ELEMENT_TYPE = [
        ("paragraph", "Paragraph"), 
        ("note", "Note"),
        ("example", "Example"),
        ("subsection", "Subsection"),
        ("image", "Image"),
        ("video", "Video")
    ]
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    element_type = models.CharField(max_length=16, choices=ELEMENT_TYPE)

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="app/static/app/")
    element_type = models.CharField(max_length=16, default="image")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

class MCQ(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    options = models.TextField() # concatenated string of options
    answer = models.TextField()
    hint = models.TextField(blank=True)
    element_type = models.CharField(max_length=16, default="mcq")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)

class FIB(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    hint = models.TextField(blank=True)
    element_type = models.CharField(max_length=16, default="fib")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)

class Likert(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    positive = models.TextField() 
    negative = models.TextField()
    element_type = models.CharField(max_length=16, default="likert")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

class Response(models.Model):
    QUESTION_TYPE = [
        ("mcq", "MCQ"),
        ("fib", "FIB"), 
        ("likert", "Likert")
    ]
    id = models.AutoField(primary_key=True)
    question_type = models.CharField(max_length=16, choices=QUESTION_TYPE)
    question = models.IntegerField() # references the corresponding ids in question table
    answer = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.name + ": " + self.question_type + " Q" + str(self.question)

class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)

    def __str__(self):
        return self.name