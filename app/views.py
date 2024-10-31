from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Chapter, Student, Textbook, Content, FIB, Likert, MCQ, Response, Author, Skill
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import mimetypes
import io
import zipfile
from django.conf import settings
import os 

def index(request):
    return HttpResponse("Hello, world. You're at the app index.")

def user_login(request):
    login_failed = False
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            if Author.objects.filter(user_id=user.id).exists():
                login(request, user)
                return redirect(f'/{user.id}')
            else: 
                login_failed = True
        else:
            # If authentication fails, set login_failed flag to True
            login_failed = True
    
    # # Render the login page with the form and login_failed flag
    return render(request, 'app/login.html', {'login_failed': login_failed})
    # return render(request, "app/login.html")

def user_logout(request):
    logout(request)
    
    return redirect("login")

@login_required(login_url="login")
def author_detail(request, author_id):
    author = Author.objects.get(user_id=author_id)
    textbooks = []
    for textbook_id in author.textbooks.split(', '):
        textbooks.append(Textbook.objects.get(id=textbook_id))
    
    template = loader.get_template("app/author_detail.html")
    context = {
        "author": author,
        "textbooks": textbooks,
    }
    return HttpResponse(template.render(context, request))
    
@login_required(login_url="login")
def add_textbook(request):
    new_textbook_name = request.POST.get("textbook_name")
    textbook_id = request.POST.get("textbook_id")
    user = request.user
    # print(user.id)
    if Author.objects.filter(user_id=user.id).exists():
        # print(Author.objects.get(user_id=user.id))
        new_textbook = Textbook(name=new_textbook_name)
        new_textbook.save()
        author = Author.objects.get(user_id=user.id)
        author.textbooks += ", " + str(new_textbook.id)
        author.textbooks = author.textbooks.lstrip(", ")
        author.save()
        return redirect(f'/textbooks/{new_textbook.id}')
    return HttpResponse("Not registered as an author!")

@login_required(login_url="login")
def delete_textbook(request):
    delete_textbook_id = request.POST.get("textbook_id")
    author = Author.objects.get(user_id=request.user.id)
    textbook = Textbook.objects.get(id=delete_textbook_id)
    
    new_textbooks = author.textbooks.split(", ")
    new_textbooks.remove(str(textbook.id))
    author.textbooks = ", ".join(new_textbooks)
    
    author.save()
    textbook.delete()
    return redirect(f'/{request.user.id}')

@login_required(login_url="login")
def textbook(request, textbook_id):
    textbook = Textbook.objects.get(id=textbook_id)
    published_chapters = []
    for chapter_id in textbook.published_chapters.split(', '):
        if chapter_id:
            published_chapters.append(Chapter.objects.get(id=chapter_id))

    unpublished_chapters = []
    for chapter_id in textbook.unpublished_chapters.split(', '):
        if chapter_id:
            unpublished_chapters.append(Chapter.objects.get(id=chapter_id))
        
    template = loader.get_template("app/textbook.html")
    context = {
        "textbook": textbook,
        "published_chapters": published_chapters,
        "unpublished_chapters": unpublished_chapters,
    }

    return HttpResponse(template.render(context, request))
    # return render(request, 'app/textbook.html', context)

def create_element(element, contents, chapter):
    obj = None

    if element == 'paragraph':
        content = ''.join(contents[:-1]).rstrip("\n")
        obj = Content(content=content, chapter=chapter, element_type=element)
        obj.save()
           
    elif element == 'note':
        content = ''.join(contents[1:-1]).rstrip("\n")
        obj = Content(content=content, chapter=chapter, element_type=element)
        obj.save()
    
    elif element == 'example':
        content = ''.join(contents[1:-1]).rstrip("\n")
        obj = Content(content=content, chapter=chapter, element_type=element)
        obj.save()
    
    elif element == 'subsection':
        content = contents[0].rstrip("\n")
        obj = Content(content=content, chapter=chapter, element_type=element)
        obj.save()
    
    elif element == 'image':
        content = contents[0].lstrip("Images/")
        obj = Content(content=content, chapter=chapter, element_type=element)
        obj.save()
    
    elif element == 'video':
        content = contents[0]
        obj = Content(content=content, chapter=chapter, element_type=element)
        obj.save()
    
    elif element == 'mcq':
        question = contents[0].strip('\n').split(': ')[1]
        options = []
        answer = ''
        hint = ''
        for option in contents[1:-1]:
            # print(option + "jhahaha")
            if option.startswith('correct:'):
                print(option)
                answer = option.split(':')[1]
                options.append(answer)
            else:
                option = option.strip('\n').split(':')
                options.append(option[1])
                if option[2] != '\n':
                    hint = option[2]
        # print(question, options, answer, hint)
        obj = MCQ(question=question, options=", ".join(options), answer=answer, hint=hint, chapter=chapter)
        obj.save()

    elif element == 'fib':
        question = contents[0].strip('\n').split(': ')[1]
        answer = contents[1].split(':')[1]
        hint =  contents[2].split(': ')[1].strip('\n')
        # print(question, answer, hint)
        obj = FIB(question=question, answer=answer, hint=hint, chapter=chapter)
        obj.save()

    elif element == 'likert':
        question = contents[0].strip('\n').split(': ')[1]
        negative, positive = contents[1].strip('\n').split(':')
        # print(question, positive, negative)
        obj = Likert(question=question, positive=positive, negative=negative, chapter=chapter)
        obj.save()

    if obj != None: 
        return (obj.element_type + '-' + str(obj.id))
    
@login_required(login_url="login")
def add_chapter(request):
    new_chapter_name = request.POST.get("chapter_name")          
    textbook_id = request.POST.get("textbook_id")
    textbook = Textbook.objects.get(id=textbook_id)
    new_chapter = Chapter(name=new_chapter_name, textbook=textbook)
    new_chapter.save()

    if "image_files" in request.FILES:
        image_files = request.FILES.getlist("image_files")
        for image_file in image_files:
            with open('app/static/app/' + image_file.name, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

    if "chapter_file" in request.FILES:
        uploaded_file = request.FILES["chapter_file"]

        elements = []
        current_element = None
        current_content = []

        for line in uploaded_file:
            line = line.decode('utf-8')

            if current_element == 'title':
                if not line.startswith('##'):
                    current_content.append(line.strip('\n'))
                else:
                    # elements.append(create_element(current_element, current_content, new_chapter))
                    current_element = ''
                    current_content = []
            elif current_element == 'subsection':
                if not line.startswith('----'):
                    current_content.append(line.strip('\n'))
                else:
                    elements.append(create_element(current_element, current_content, new_chapter))
                    current_element = ''
                    current_content = []
            elif line.startswith('.. page::'):
                component_name = line.split(':')[-1].strip('\n')
            elif line.startswith('#'):
                current_element = 'title'
            elif line.startswith('.. note::'):
                if current_element:
                    elements.append(create_element(current_element, current_content, new_chapter))
                current_element = 'note'
                current_content = []
            elif line.startswith('::'):
                if current_element:
                    elements.append(create_element(current_element, current_content, new_chapter))
                current_element = 'example'
                current_content = []
            elif line.startswith('----'):
                if current_element:
                    elements.append(create_element(current_element, current_content, new_chapter))
                current_element = 'subsection'
                current_content = []
            elif line.startswith('.. image:: '):
                if current_element:
                    elements.append(create_element(current_element, current_content, new_chapter))
                current_element = 'image'
                current_content = [line.lstrip('.. image:: ').strip('\n')]
            elif line.startswith('.. youtube:: '):
                if current_element:
                    elements.append(create_element(current_element, current_content, new_chapter))
                current_element = 'video'
                current_content = [line.lstrip('.. youtube:: ').strip('\n')]
            elif line.startswith('.. mcq:'):
                if current_element:
                    elements.append(create_element(current_element, current_content, new_chapter))
                current_element = 'mcq'
                current_content = [line]
            elif line.startswith('.. fillintheblank:'):
                if current_element:
                    elements.append(create_element(current_element, current_content, new_chapter))
                current_element = 'fib'
                current_content = [line]
            elif line.startswith('.. likert::'):
                if current_element:
                    elements.append(create_element(current_element, current_content, new_chapter))
                current_element = 'likert'
                current_content = [line]
            elif line.startswith('[Next: ') or line.startswith('[Prev: `'):
                continue
            elif not line.startswith((' ', '\t', '\n')) and current_element != 'paragraph':
                if current_element:
                    elements.append(create_element(current_element, current_content, new_chapter))
                current_element = 'paragraph'
                current_content = [line]
            else:
                if current_element:
                    current_content.append(line.lstrip('    '))

        if current_element:
            elements.append(create_element(current_element, current_content, new_chapter))
        
        print(elements)

        new_chapter.elements = ', '.join(elements)

    new_chapter.save()
    textbook.unpublished_chapters += ", " + str(new_chapter.id)
    textbook.unpublished_chapters = textbook.unpublished_chapters.lstrip(", ")
    
    textbook.save()
    return redirect(f'/chapters/{new_chapter.id}')

@login_required(login_url="login")
def delete_chapter(request):
    delete_chapter_id = request.POST.get("chapter_id")
    textbook_id = request.POST.get("textbook_id")
    textbook = Textbook.objects.get(id=textbook_id)
    chapter = Chapter.objects.get(id=delete_chapter_id)

    if chapter.isPublished:
        new_chapters = textbook.published_chapters.split(", ")
        new_chapters.remove(str(chapter.id))
        textbook.published_chapters = ", ".join(new_chapters)
    else:
        new_chapters = textbook.unpublished_chapters.split(", ")
        new_chapters.remove(str(chapter.id))
        textbook.unpublished_chapters = ", ".join(new_chapters)
    
    textbook.save()
    chapter.delete()
    return redirect(f'/textbooks/{textbook_id}')

@login_required(login_url="login")
def edit_textbook(request, textbook_id):
    textbook = Textbook.objects.get(id=textbook_id)
    published_chapters = []
    for chapter_id in textbook.published_chapters.split(', '):
        if chapter_id:
            published_chapters.append(Chapter.objects.get(id=chapter_id))

    unpublished_chapters = []
    for chapter_id in textbook.unpublished_chapters.split(', '):
        if chapter_id:
            unpublished_chapters.append(Chapter.objects.get(id=chapter_id))
        
    # template = loader.get_template("app/edit_textbook.html")
    context = {
        "textbook": textbook,
        "published_chapters": published_chapters,
        "unpublished_chapters": unpublished_chapters,
    }
    if request.method == "POST":
        submitted_chapters = request.POST.getlist("chapters")
        new_published_chapters = ""
        new_unpublished_chapters = ""
        i = 0
        while i < len(submitted_chapters):
            if submitted_chapters[i] == "::published::":
                while submitted_chapters[i+1] != "::unpublished::":
                    i += 1
                    new_published_chapters += submitted_chapters[i] + ", "
                    chapter = Chapter.objects.get(id=submitted_chapters[i])
                    chapter.isPublished = True
                    chapter.save()
                i += 2
            if i < len(submitted_chapters):
                new_unpublished_chapters += submitted_chapters[i] + ", "
                chapter = Chapter.objects.get(id=submitted_chapters[i])
                chapter.isPublished = False
                chapter.save()
            i += 1

        new_published_chapters = new_published_chapters.rstrip(", ")
        new_unpublished_chapters = new_unpublished_chapters.rstrip(", ")
        textbook.published_chapters = new_published_chapters
        textbook.unpublished_chapters = new_unpublished_chapters
        textbook.save()
        print(new_published_chapters)
        print(new_unpublished_chapters)  
        return redirect("/textbooks/" + str(textbook.id))


    # return HttpResponse(template.render(context, request))
    return render(request, 'app/edit_textbook.html', context)

@login_required(login_url="login")
def edit_chapter(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    elements = dict()
    if chapter.elements != "":
        for element in chapter.elements.split(', '):
            element_type, element_id = element.split('-')
            if element_type == "paragraph" or element_type == "note" or element_type == "example" or element_type =="subsection" or element_type == "image" or element_type == "video":
                elements[Content.objects.get(id = element_id)] = ""
            elif element_type == "image":
                elements[Image.objects.get(id = element_id)] = ""
            elif element_type == "mcq":
                question = MCQ.objects.get(id = element_id)
                skill_names = ""
                if question.skills != "":
                    for skill_id in question.skills.split(", "):
                        skill_names += Skill.objects.get(id=skill_id).name + ", "
                elements[question] = skill_names.rstrip(", ")
            elif element_type == "fib":
                question = FIB.objects.get(id = element_id)
                skill_names = ""
                if question.skills != "":
                    for skill_id in question.skills.split(", "):
                        skill_names += Skill.objects.get(id=skill_id).name + ", "
                elements[question] = skill_names.rstrip(", ")
            elif element_type == "likert":
                elements[Likert.objects.get(id = element_id)] = ""

    context = {
        "chapter": chapter,
        "elements": elements,
    }

    if request.method == "POST":
        new_chapter_elements = ""
        submitted_elements = request.POST.getlist("elements")
        new_chapter_skills = []
        image_counter = 0
        images = request.FILES.getlist('elements')
        i = 0
        while i < len(submitted_elements):
            # print(submitted_elements[i])
            
            if submitted_elements[i].startswith("paragraph::") or submitted_elements[i].startswith("note::") or submitted_elements[i].startswith("example::") or submitted_elements[i].startswith("video::") or submitted_elements[i].startswith("subsection::"):
                element_type, element_id = submitted_elements[i].split("::")
                content = submitted_elements[i+1]
                if element_id != "-1": 
                    element_obj = Content.objects.get(id=element_id) 
                    element_obj.content=content
                else:
                    if element_type == "paragraph":
                        element_obj = Content(content=content, chapter=chapter, element_type="paragraph")
                    elif element_type == "note":
                        element_obj = Content(content=content, chapter=chapter, element_type="note")
                    elif element_type == "example":
                        element_obj = Content(content=content, chapter=chapter, element_type="example")
                    elif element_type == "subsection":
                        element_obj = Content(content=content, chapter=chapter, element_type="subsection")
                    else:
                        element_obj = Content(content=content, chapter=chapter, element_type="video")
                element_obj.save()
                new_chapter_elements += element_type + "-" + str(element_obj.id) + ", "
                i += 1
            elif submitted_elements[i].startswith("image::"):
                element_type, element_id = submitted_elements[i].split("::")
                if element_id != "-1":
                    element_obj = Content.objects.get(id=element_id) 
                    if (i+1 < len(submitted_elements)):
                        if(submitted_elements[i+1] == ""): # existing element with no change - do nothing 
                            i += 1
                        else: # new image is uploaded -> save new image and update to new image
                            # 1. update image file name
                            image_file = images[image_counter]
                            element_obj.content=image_file
                            # 2. save image to local 
                            with open('app/static/app/' + image_file.name, 'wb+') as destination:
                                for chunk in image_file.chunks():
                                    destination.write(chunk)
                            image_counter += 1
                    else: # new image is uploaded -> save new image and update to new image
                        # 1. update image file name
                        image_file = images[image_counter]
                        element_obj.content=image_file
                        # 2. save image to local 
                        with open('app/static/app/' + image_file.name, 'wb+') as destination:
                            for chunk in image_file.chunks():
                                destination.write(chunk)
                        image_counter += 1
                       
                else: 
                    if (i+1 < len(submitted_elements)):
                        if(submitted_elements[i+1] == ""): # new element with no file 
                            element_obj = Content(content="", chapter=chapter, element_type="image")
                            i += 1
                        else: # new element with file
                            # 1. update image file name
                            image_file = images[image_counter]
                            element_obj = Content(content=image_file, chapter=chapter, element_type="image")
                            # 2. save image to local 
                            with open('app/static/app/' + image_file.name, 'wb+') as destination:
                                for chunk in image_file.chunks():
                                    destination.write(chunk)
                            image_counter += 1
                    else:
                        # 1. update image file name
                        image_file = images[image_counter]
                        element_obj = Content(content=image_file, chapter=chapter, element_type="image")
                        # 2. save image to local 
                        with open('app/static/app/' + image_file.name, 'wb+') as destination:
                            for chunk in image_file.chunks():
                                destination.write(chunk)
                        image_counter += 1
                    

                element_obj.save()
                new_chapter_elements += element_type + "-" + str(element_obj.id) + ", "

            elif submitted_elements[i].startswith("mcq::"):
                element_type, element_id = submitted_elements[i].split("::")
                question = submitted_elements[i+1]
                options = submitted_elements[i+2]
                answer = submitted_elements[i+3]
                hint = submitted_elements[i+4]
                skills = ""
                if submitted_elements[i+5] != "":
                    for skill_name in submitted_elements[i+5].split(", "):
                        if not Skill.objects.filter(name=skill_name, textbook=chapter.textbook):
                            skill = Skill(name=skill_name, textbook=chapter.textbook)
                            skill.save()
                        skill_id = str(Skill.objects.get(name=skill_name, textbook=chapter.textbook).id)
                        skills += skill_id + ", "
                        if skill_id not in new_chapter_skills:
                            new_chapter_skills.append(skill_id)
                    skills = skills.rstrip(", ")
                
                if element_id != "-1": 
                    element_obj = MCQ.objects.get(id=element_id)
                    element_obj.question = question
                    element_obj.options = options
                    element_obj.answer = answer
                    element_obj.hint = hint
                    element_obj.skills = skills

                else:
                    element_obj = MCQ(question=question, options=options, answer=answer, hint=hint, skills=skills, chapter=chapter, element_type="mcq")

                element_obj.save()
                new_chapter_elements += element_type + "-" + str(element_obj.id) + ", "
                i += 5
            elif submitted_elements[i].startswith("fib::"):
                element_type, element_id = submitted_elements[i].split("::")
                question = submitted_elements[i+1]
                answer = submitted_elements[i+2]
                hint = submitted_elements[i+3]
                skills = ""
                if submitted_elements[i+4] != "":
                    for skill_name in submitted_elements[i+4].split(", "):
                        if not Skill.objects.filter(name=skill_name, textbook=chapter.textbook):
                            skill = Skill(name=skill_name, textbook=chapter.textbook)
                            skill.save()
                        skill_id = str(Skill.objects.get(name=skill_name, textbook=chapter.textbook).id)
                        skills += skill_id + ", "
                        if skill_id not in new_chapter_skills:
                            new_chapter_skills.append(skill_id)
                    skills = skills.rstrip(", ")

                if element_id != "-1": 
                    element_obj = FIB.objects.get(id=element_id)
                    element_obj.question = question
                    element_obj.answer = answer
                    element_obj.hint = hint
                    element_obj.skills = skills

                else:
                    element_obj = FIB(question=question, answer = answer, hint = hint, skills=skills, chapter=chapter, element_type="fib")

                element_obj.save()
                new_chapter_elements += element_type + "-" + str(element_obj.id) + ", "
                i += 4
            elif submitted_elements[i].startswith("likert::"):
                element_type, element_id = submitted_elements[i].split("::")
                question = submitted_elements[i+1]
                negative = submitted_elements[i+2]
                positive = submitted_elements[i+3]
                if element_id != "-1": 
                    element_obj = Likert.objects.get(id=element_id)
                    element_obj.question = question
                    element_obj.positive = positive
                    element_obj.negative = negative

                else:
                    element_obj = Likert(question=question, positive=positive, negative=negative, chapter=chapter, element_type="likert")

                element_obj.save()
                new_chapter_elements += element_type + "-" + str(element_obj.id) + ", "
            
                i += 3
            i+=1
        
        # print(new_chapter_skills)
        
        chapter.elements = new_chapter_elements.rstrip(", ")
        if len(new_chapter_skills) > 0:
            chapter.skills = ", ".join(new_chapter_skills)
        chapter.save()
        # Redirect to a new URL after saving the data
        return redirect("/chapters/" + str(chapter.id)) 

    # return HttpResponse(template.render(context, request))
    return render(request, 'app/edit_chapter.html', context)

@login_required(login_url="login")
def chapter(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    elements = dict()
    if chapter.elements != "":
        for element in chapter.elements.split(', '):
            element_type, element_id = element.split('-')
            if element_type == "paragraph" or element_type == "note" or element_type == "example" or element_type =="subsection" or element_type == "image" or element_type == "video":
                elements[Content.objects.get(id = element_id)] = ""
            elif element_type == "image":
                elements[Image.objects.get(id = element_id)] = ""
            elif element_type == "mcq":
                question = MCQ.objects.get(id = element_id)
                skill_names = ""
                if question.skills != "":
                    for skill_id in question.skills.split(", "):
                        skill_names += Skill.objects.get(id=skill_id).name + ", "
                elements[question] = skill_names.rstrip(", ")
            elif element_type == "fib":
                question = FIB.objects.get(id = element_id)
                skill_names = ""
                if question.skills != "":
                    for skill_id in question.skills.split(", "):
                        skill_names += Skill.objects.get(id=skill_id).name + ", "
                elements[question] = skill_names.rstrip(", ")
            elif element_type == "likert":
                elements[Likert.objects.get(id = element_id)] = ""

    context = {
        "chapter": chapter,
        "elements": elements,
    }

    return render(request, 'app/chapter.html', context)

@login_required(login_url="login")
def chapter_response(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    
    students = []
    for student in Student.objects.all():
        textbooks = student.textbooks.split(', ')
        if str(chapter.textbook.id) in textbooks:
            students.append(student)

    skills = dict()
    responses = dict()
    for response in Response.objects.filter(chapter=chapter_id):
        if response.question_type == "mcq":
            question = MCQ.objects.get(id=response.question)
            if question not in skills.keys(): 
                question_skills = []
                if question.skills != "":
                    for skill_id in question.skills.split(", "):
                        question_skills.append(Skill.objects.get(id=skill_id).name)
                    skills[question] = ', '.join(question_skills)
                else:
                    skills[question] = "No related skills specified."
            responses[response] = question
        elif response.question_type == "fib":
            question = FIB.objects.get(id=response.question)
            if question not in skills.keys(): 
                question_skills = []
                if question.skills != "":
                    for skill_id in question.skills.split(", "):
                        question_skills.append(Skill.objects.get(id=skill_id).name)
                    skills[question] = ', '.join(question_skills)
                else:
                    skills[question] = "No related skills specified."
            responses[response] = question
        elif response.question_type == "likert":
            responses[response] = Likert.objects.get(id=response.question)
    
    print(skills)
    context = {
        "chapter": chapter,
        "students": students,
        "responses": responses,
        "skills": skills
    }
    return render(request, 'app/chapter_response.html', context)

@login_required(login_url="login")
def chapter_summary(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    responses = dict()
    students = []
    for response in Response.objects.filter(chapter=chapter_id):
        if response.question_type == "mcq":
            question = MCQ.objects.get(id=response.question)
            if question not in responses.keys():
                responses[question] = [dict()]
                for option in question.options.split(', '):
                    responses[question][0][option] = 0    
        elif response.question_type == "fib":
            question = FIB.objects.get(id=response.question)
        elif response.question_type == "likert":
            question = Likert.objects.get(id=response.question)
            if question not in responses.keys():
                responses[question] = [{"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}]
        
        answer = response.answer
        if question not in responses.keys():
            responses[question] = [{answer: 1}]
        else: 
            answers = responses[question][0]
            if answer not in answers.keys():
                answers[answer] = 1
            else:
                answers[answer] += 1
        
        if response.student not in students:
            students.append(response.student)

    # print(responses)
    total_responses = len(students)
    for question in responses:
        if question.element_type != "likert":
            # Calculate the percentage correct
            correct_answer = question.answer
            for answer in responses[question][0]:
                if answer == correct_answer:
                    total_correct = responses[question][0][answer]
            responses[question].append(round(total_correct/total_responses * 100, 2))

            # Find the related skills and add to the question
            if question.skills != "":
                question_skills = []
                for skill_id in question.skills.split(', '):
                    question_skills.append(Skill.objects.get(id=skill_id).name)
                responses[question].append(', '.join(question_skills))
            else:
                responses[question].append('No related skills specified.')
    print(responses)

    context = {
        "chapter": chapter,
        "responses": responses,
        "total_responses": total_responses,
    }
    
    return render(request, 'app/chapter_summary.html', context)

@login_required(login_url="login")
def chapter_matrix(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    matrix = dict()
    skills = dict()
    questions = []
    if chapter.skills != "":
        for skill_id in chapter.skills.split(", "):
            skills[Skill.objects.get(id=skill_id)] = 0
        # print(skills)
        for response in Response.objects.filter(chapter=chapter_id):
            if response.student not in matrix:
                student_ratings = dict()
                for skill in skills.keys():
                    student_ratings[skill] = [0]
                matrix[response.student] = student_ratings

            student_ratings = matrix[response.student]
            
            if response.question_type == "mcq":
                question = MCQ.objects.get(id=response.question)
            elif response.question_type == "fib":
                question = FIB.objects.get(id=response.question)
            else:
                continue
            
            if question not in questions:
                for skill_id in question.skills.split(", "):
                    skills[Skill.objects.get(id=skill_id)] += 1
                questions.append(question)

            if question.answer == response.answer:
                for skill_id in question.skills.split(", "):
                    student_ratings[Skill.objects.get(id=skill_id)][0] += 1
        
        # print(matrix)
        # print(skills)
        for student in matrix.keys():
            for skill in matrix[student].keys():
                matrix[student][skill].append(skills[skill])
        # print(matrix)

    # print(matrix)
    average_scores = dict()
    for student in matrix.keys():
        for skill in matrix[student].keys():
            if skill not in average_scores.keys():
                average_scores[skill] = matrix[student][skill][0]
            else:
                average_scores[skill] += matrix[student][skill][0]

    for score in average_scores.keys():
        average_scores[score] = round(average_scores[score] / len(matrix), 2)
    # print(average_scores)

    average_scores_percent = dict()
    for score in average_scores.keys():
        # print(score)
        average_scores_percent[score] = round(average_scores[score]/skills[score] * 100)
    # print(average_scores_percent)

    context = {
        "chapter": chapter,
        "skills": skills,
        "matrix": matrix,
        "average_scores": average_scores,
        "average_scores_percent": average_scores_percent,
        "total_responses": len(matrix)
    }
    return render(request, 'app/chapter_matrix.html', context)

@login_required(login_url="login")
def download_chapter(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    image_files = []
    content = ".. page::" + chapter.textbook.name + ":" + chapter.name.lower().replace(' ', '-') + "\n\n"
    content += "########################\n" + chapter.name + "\n" + "########################\n\n"
    if chapter.elements != "":
        for element in chapter.elements.split(', '):
            element_type, element_id = element.split('-')
            if element_type == "paragraph":
                content += Content.objects.get(id = element_id).content + "\n\n"
            elif element_type == "note":
                note = Content.objects.get(id = element_id).content
                lines = note.split('\n')
                lines_with_space = ['   ' + line for line in lines]
                content += ".. note:: \n\n" + '\n'.join(lines_with_space) + "\n\n"
            elif element_type == "example":
                example = Content.objects.get(id = element_id).content
                lines = example.split('\n')
                lines_with_space = ['   ' + line for line in lines]
                content += "::\n\n" + '\n'.join(lines_with_space) + "\n\n"
            elif element_type =="subsection":
                content += "----------------------------\n" + Content.objects.get(id = element_id).content + "\n----------------------------\n\n"
            elif element_type == "image":
                image_name = Content.objects.get(id = element_id).content
                content += ".. image:: Images/" + image_name + "\n" + "   :width: 10cm \n   :align: center\n\n"
                image_files.append(image_name)
            elif element_type == "video":
                content += ".. youtube:: " + Content.objects.get(id = element_id).content + "\n" + "   :align: left\n\n"
            elif element_type == "mcq":
                mcq = MCQ.objects.get(id = element_id)
                content += ".. mcq:" + chapter.name.lower().replace(' ', '-') + ": " + mcq.question + "\n"
                for option in mcq.options.split(', '):
                    if mcq.answer == option: 
                        content += "   :correct:" + option + ":Correct!" + "\n"
                    else: 
                        content += "   :" + option + ":" + mcq.hint + "\n"
                content += "\n"
            elif element_type == "fib":
                fib = FIB.objects.get(id = element_id)
                content += ".. fillintheblank:" + chapter.name.lower().replace(' ', '-') + ": " + fib.question + "\n"
                content += "   correct:" + fib.answer + ": Correct!" + "\n"
                content += "   incorrect:x: " + fib.hint + "\n"
                content += "\n"
            elif element_type == "likert":
                likert = Likert.objects.get(id = element_id)
                content += ".. likert::" + chapter.name.lower().replace(' ', '-') + ": " + likert.question + "\n"
                content += "   " + likert.negative + ":" + likert.positive + "\n"
                content += "\n"

    chapters = chapter.textbook.published_chapters.split(', ')
    idx = chapters.index(str(chapter_id))
    if idx > 0:
        prev_chapter = Chapter.objects.get(id=chapters[idx - 1])
        print(prev_chapter)
        content += "[Prev: `" + prev_chapter.name + " <" + prev_chapter.name + ".html>`_]"
    if idx < len(chapters)-1:
        next_chapter = Chapter.objects.get(id=chapters[idx + 1])
        content += "[Next: `" + next_chapter.name + " <" + next_chapter.name.lower().replace(" ", "-") + ".html>`_]"
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        # Add the compiled file content directly to the ZIP
        file_name = chapter.name.lower().replace(" ", "-") + ".erst"
        zf.writestr(file_name, content)

        # Add each image file
        for image in image_files:
            image_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', image)
            if os.path.exists(image_path):
                zf.write(image_path, f"Images/{os.path.basename(image_path)}")

    # Ensure the ZIP is fully written
    zip_buffer.seek(0)

    # Prepare the response
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={chapter.name.lower().replace(" ", "-")}.zip'

    return response

@login_required(login_url="login")
def publish_chapter(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    chapter.isPublished = True
    chapter.save()
    print(chapter.isPublished)

    textbook = chapter.textbook
    unpublished_chapters = textbook.unpublished_chapters.split(', ')
    unpublished_chapters.remove(str(chapter.id))
    textbook.unpublished_chapters = ', '.join(unpublished_chapters)
    published_chapters = textbook.published_chapters.split(', ')
    published_chapters.append(str(chapter.id))
    textbook.published_chapters = ', '.join(published_chapters)
    textbook.save()
    return redirect("/chapters/" + str(chapter.id)) 

@login_required(login_url="login")
def unpublish_chapter(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    chapter.isPublished = False
    chapter.save()
    print(chapter.isPublished)

    textbook = chapter.textbook
    published_chapters = textbook.published_chapters.split(', ')
    published_chapters.remove(str(chapter.id))
    textbook.published_chapters = ', '.join(published_chapters)
    unpublished_chapters = textbook.unpublished_chapters.split(', ')
    unpublished_chapters.append(str(chapter.id))
    textbook.unpublished_chapters = ', '.join(unpublished_chapters)
    textbook.save()

    return redirect("/chapters/" + str(chapter.id)) 