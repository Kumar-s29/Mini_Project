from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from django.contrib import messages
from django.views import generic
from .models import Homework
from .forms import DashboardForm
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
import json


# Create your views here.
def home(request):
    return render(request, "dashboard/home.html")


def custom_logout(request):
    logout(request)
    return render(request, "dashboard/logout.html")


@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user,
                title=request.POST["title"],
                description=request.POST["description"],
            )
            notes.save()
        messages.success(
            request, f"Notes Added from {request.user.username} Successfully!"
        )
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {"notes": notes, "form": form}
    return render(request, "dashboard/notes.html", context)


@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes


@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user=request.user,
                subject=request.POST["subject"],
                title=request.POST["title"],
                description=request.POST["description"],
                due=request.POST["due"],
                is_finished=finished,
            )
            homeworks.save()
            messages.success(request, f"Homework Added from {request.user.username}!!")
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {"homeworks": homework, "homework_done": homework_done, "form": form}
    return render(request, "dashboard/homework.html", context)


@login_required
def update_homework(request, pk=None):

    homework = get_object_or_404(Homework, pk=pk)

    homework.is_finished = not homework.is_finished
    homework.save()

    return redirect("homework")


@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        result_list = []
        
        try:
            # Method 1: Scrape YouTube search results page
            search_url = f"https://www.youtube.com/results?search_query={quote(text)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Extract JSON data from the page
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find the script tag containing ytInitialData
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.string and 'var ytInitialData = ' in script.string:
                        # Extract JSON data
                        json_str = script.string.split('var ytInitialData = ')[1]
                        json_str = json_str.split(';</script>')[0]
                        json_str = json_str.rstrip(';')
                        
                        try:
                            data = json.loads(json_str)
                            
                            # Navigate through the JSON structure
                            contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
                            
                            for content in contents:
                                item_section = content.get('itemSectionRenderer', {}).get('contents', [])
                                
                                for item in item_section[:10]:
                                    video_data = item.get('videoRenderer', {})
                                    
                                    if video_data:
                                        video_id = video_data.get('videoId', '')
                                        title = video_data.get('title', {}).get('runs', [{}])[0].get('text', 'N/A')
                                        
                                        # Get duration
                                        duration_text = video_data.get('lengthText', {}).get('simpleText', 'N/A')
                                        
                                        # Get channel name
                                        channel = video_data.get('ownerText', {}).get('runs', [{}])[0].get('text', 'N/A')
                                        
                                        # Get view count
                                        view_count = video_data.get('viewCountText', {}).get('simpleText', 'N/A')
                                        
                                        # Get published time
                                        published = video_data.get('publishedTimeText', {}).get('simpleText', 'N/A')
                                        
                                        # Get description
                                        description_snippets = video_data.get('detailedMetadataSnippets', [{}])
                                        description = ''
                                        if description_snippets:
                                            snippet_runs = description_snippets[0].get('snippetText', {}).get('runs', [])
                                            description = ''.join([run.get('text', '') for run in snippet_runs])[:200]
                                        
                                        result_dict = {
                                            "input": text,
                                            "title": title,
                                            "duration": duration_text,
                                            "thumbnail": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
                                            "channel": channel,
                                            "link": f"https://www.youtube.com/watch?v={video_id}",
                                            "views": view_count,
                                            "published": published,
                                            "description": description if description else "No description available"
                                        }
                                        result_list.append(result_dict)
                                        
                                        if len(result_list) >= 10:
                                            break
                                
                                if len(result_list) >= 10:
                                    break
                                    
                        except json.JSONDecodeError:
                            pass
                        
                        break
            
            if result_list:
                context = {"form": form, "results": result_list}
                return render(request, "dashboard/youtube.html", context)
            else:
                messages.warning(request, f"No results found for '{text}'. Please try a different search term.")
                context = {"form": form, "results": []}
                return render(request, "dashboard/youtube.html", context)
                
        except Exception as e:
            messages.error(request, f"Error searching YouTube. Please try again later.")
            context = {"form": form, "results": []}
            return render(request, "dashboard/youtube.html", context)
    else:
        form = DashboardForm()
    context = {"form": form}
    return render(request, "dashboard/youtube.html", context)


@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user=request.user,
                title=request.POST["title"],
                is_finished=finished,
            )
            todos.save()
            messages.success(request, f"Todo added from {request.user.username}!!")

    else:
        form = TodoForm()

    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {"form": form, "todos": todo, "todo_done": todos_done}
    return render(request, "dashboard/todo.html", context)


@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect("todo")


@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


import requests

def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get("text")  # Use get() to safely retrieve form data
        result_list = []
        try:
            url = "https://www.googleapis.com/books/v1/volumes?q=" + text
            r = requests.get(url, timeout=10)
            answer = r.json()
            if "items" in answer:  # Check if "items" key exists in the JSON response
                for item in answer["items"][:10]:  # Limit to 10 items
                    volume_info = item.get("volumeInfo", {})
                    result_dict = {
                        "title": volume_info.get("title", "Title Not Available"),
                        "subtitle": volume_info.get("subtitle", "Subtitle Not Available"),
                        "description": volume_info.get("description", "Description Not Available"),
                        "count": volume_info.get("pageCount", "Page Count Not Available"),
                        "categories": volume_info.get("categories", []),
                        "rating": volume_info.get("pageRating", "Rating Not Available"),
                        "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                        "preview": volume_info.get("previewLink", "Preview Link Not Available"),
                    }
                    result_list.append(result_dict)
            else:
                result_list = []  # Handle case where "items" key is missing or empty
        except Exception as e:
            messages.error(request, f"Error searching books: Unable to fetch results. Please try again.")
            result_list = []
        
        context = {"form": form, "results": result_list}
        return render(request, "dashboard/books.html", context)
    else:
        form = DashboardForm()
        context = {"form": form}
        return render(request, "dashboard/books.html", context)


def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        try:
            url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
            r = requests.get(url, timeout=10)
            answer = r.json()
            phonetics = answer[0]["phonetics"][0]["text"]
            audio = answer[0]["phonetics"][0]["audio"]
            definition = answer[0]["meanings"][0]["definitions"][0]["definition"]
            example = answer[0]["meanings"][0]["definitions"][0]["example"]
            synonyms = answer[0]["meanings"][0]["definitions"][0]["synonyms"]
            context = {
                "form": form,
                "input": text,
                "phonetics": phonetics,
                "audio": audio,
                "definition": definition,
                "example": example,
                "synonyms": synonyms,
            }
        except Exception as e:
            messages.error(request, f"Word not found or error occurred. Please try another word.")
            context = {"form": form, "input": ""}
        return render(request, "dashboard/dictionary.html", context)

    else:
        form = DashboardForm()
        context = {"form": form}

    return render(request, "dashboard/dictionary.html", context)


def wiki(request):
    if request.method == "POST":
        text = request.POST["text"]
        form = DashboardForm(request.POST)
        try:
            search = wikipedia.page(text)
            context = {
                "form": form,
                "title": search.title,
                "link": search.url,
                "details": search.summary,
            }
        except wikipedia.exceptions.DisambiguationError as e:
            messages.error(request, f"Multiple results found. Please be more specific. Suggestions: {', '.join(e.options[:5])}")
            context = {"form": form}
        except wikipedia.exceptions.PageError:
            messages.error(request, f"No Wikipedia page found for '{text}'. Please try another search.")
            context = {"form": form}
        except Exception as e:
            messages.error(request, f"Error searching Wikipedia. Please try again.")
            context = {"form": form}
        return render(request, "dashboard/wiki.html", context)
    else:
        form = DashboardForm()  # type: ignore
        context = {
            "form": form,
        }

    return render(request, "dashboard/wiki.html", context)


def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if "measurement" in request.POST and request.POST["measurement"] == "length":
            measurement_form = ConversionLengthForm()
            context = {"form": form, "m_form": measurement_form, "input": True}
            if "input" in request.POST and "measure1" in request.POST and "measure2" in request.POST:
                first = request.POST["measure1"]
                second = request.POST["measure2"]
                input = request.POST["input"]
                answer = ""
                if input and int(input) >= 0:
                    if first == "yard" and second == "foot":
                        answer = f"{input} yard = {int(input) * 3} foot"
                    if first == "foot" and second == "yard":
                        answer = f"{input} foot = {int(input) / 3} yard"
                context = {
                    "form": form,
                    "m_form": measurement_form,
                    "input": True,
                    "answer": answer,
                }
        if "measurement" in request.POST and request.POST["measurement"] == "mass":
            measurement_form = ConversionMassForm()
            context = {"form": form, "m_form": measurement_form, "input": True}
            if "input" in request.POST and "measure1" in request.POST and "measure2" in request.POST:
                first = request.POST["measure1"]
                second = request.POST["measure2"]
                input = request.POST["input"]
                answer = ""
                if input and int(input) >= 0:
                    if first == "pound" and second == "kilogram":
                        answer = f"{input} pound = {int(input) * 0.453592} kilogram"
                    if first == "kilogram" and second == "pound":
                        answer = f"{input} kilogram = {int(input) * 2.20462} pound"
                context = {
                    "form": form,
                    "m_form": measurement_form,
                    "input": True,
                    "answer": answer,
                }
    else:
        form = ConversionForm()
        context = {"form": form, "input": False}
    return render(request, "dashboard/conversion.html", context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}! You can now log in.")
            return redirect("login")
        else:
            # Display form errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "dashboard/register.html", context)


@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    
    # Calculate study streak and points
    profile_obj, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Extra stats for premium profile
    total_notes = Notes.objects.filter(user=request.user).count()
    total_exams = Exam.objects.filter(user=request.user).count()
    
    grades_list = Grade.objects.filter(user=request.user)
    total_obtained = sum(g.marks_obtained for g in grades_list)
    total_possible = sum(g.total_marks for g in grades_list)
    average = (total_obtained / total_possible * 100) if total_possible > 0 else 0

    context = {
        "homeworks": homeworks,
        "todos": todos,
        "homework_done": len(homeworks) == 0,
        "todos_done": len(todos) == 0,
        "streak": profile_obj.study_streak,
        "points": profile_obj.total_points,
        "total_notes": total_notes,
        "total_exams": total_exams,
        "average": round(average, 1),
    }
    return render(request, "dashboard/profile.html", context)

# --- NEW FEATURES ---

@login_required
def grades(request):
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.user = request.user
            grade.save()
            messages.success(request, "Grade added successfully!")
            return redirect('grades')
    else:
        form = GradeForm()
    
    grades_list = Grade.objects.filter(user=request.user).order_by('-date_added')
    
    # Calculate GPA or Average
    total_obtained = sum(g.marks_obtained for g in grades_list)
    total_possible = sum(g.total_marks for g in grades_list)
    average = (total_obtained / total_possible * 100) if total_possible > 0 else 0
    
    context = {"form": form, "grades": grades_list, "average": round(average, 2)}
    return render(request, "dashboard/grades.html", context)

@login_required
def delete_grade(request, pk):
    get_object_or_404(Grade, pk=pk, user=request.user).delete()
    return redirect('grades')

@login_required
def exams(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.user = request.user
            exam.save()
            messages.success(request, "Exam scheduled successfully!")
            return redirect('exams')
    else:
        form = ExamForm()
    
    exams_list = Exam.objects.filter(user=request.user).order_by('date')
    context = {"form": form, "exams": exams_list}
    return render(request, "dashboard/exams.html", context)

@login_required
def delete_exam(request, pk):
    get_object_or_404(Exam, pk=pk, user=request.user).delete()
    return redirect('exams')

@login_required
def timetable(request):
    if request.method == "POST":
        form = TimetableForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Class added to timetable!")
            return redirect('timetable')
    else:
        form = TimetableForm()
    
    # Organize by day
    schedule = {}
    for day_id, day_name in Timetable.DAYS:
        schedule[day_name] = Timetable.objects.filter(user=request.user, day=day_id).order_by('start_time')
    
    context = {"form": form, "schedule": schedule}
    return render(request, "dashboard/timetable.html", context)

@login_required
def delete_timetable(request, pk):
    get_object_or_404(Timetable, pk=pk, user=request.user).delete()
    return redirect('timetable')

@login_required
def flashcards(request):
    if request.method == "POST":
        form = FlashcardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request, "Flashcard created!")
            return redirect('flashcards')
    else:
        form = FlashcardForm()
    
    cards = Flashcard.objects.filter(user=request.user).order_by('subject')
    context = {"form": form, "cards": cards}
    return render(request, "dashboard/flashcards.html", context)

@login_required
def delete_flashcard(request, pk):
    get_object_or_404(Flashcard, pk=pk, user=request.user).delete()
    return redirect('flashcards')

@login_required
def analytics(request):
    # Prepare data for Chart.js
    homework_total = Homework.objects.filter(user=request.user).count()
    homework_done = Homework.objects.filter(user=request.user, is_finished=True).count()
    
    todo_total = Todo.objects.filter(user=request.user).count()
    todo_done = Todo.objects.filter(user=request.user, is_finished=True).count()
    
    # Grades data
    grades = Grade.objects.filter(user=request.user).order_by('date_added')
    grade_labels = [g.subject for g in grades]
    grade_values = [float(g.marks_obtained/g.total_marks*100) for g in grades]
    
    context = {
        "hw_done": homework_done,
        "hw_pending": homework_total - homework_done,
        "todo_done": todo_done,
        "todo_pending": todo_total - todo_done,
        "grade_labels": json.dumps(grade_labels),
        "grade_values": json.dumps(grade_values),
    }
    return render(request, "dashboard/analytics.html", context)

@login_required
def focus_timer(request):
    return render(request, "dashboard/focus.html")

@login_required
def whiteboard(request):
    return render(request, "dashboard/whiteboard.html")

@login_required
def ai_assistant(request):
    summary = ""
    if request.method == "POST":
        text = request.POST.get("text", "")
        action = request.POST.get("action", "summarize")
        
        # MOCK AI Logic (In a real app, you'd call OpenAI/Gemini here)
        if action == "summarize":
            summary = f"AI Summary: This text discusses '{text[:50]}...'. Key points include its primary focus on learning and development."
        elif action == "quiz":
            summary = f"AI Generated Quiz: 1. What is the main theme of '{text[:20]}'? 2. Explain the significance of the mentioned concepts."
            
    return render(request, "dashboard/ai_assistant.html", {"summary": summary})

from django.http import HttpResponse
from django.template.loader import get_template
# Note: For real PDF generation, you'd need xhtml2pdf or similar installed
# I'll provide a simple HTML-to-file fallback for now to avoid crashes if lib is missing

def export_note_pdf(request, pk):
    note = get_object_or_404(Notes, pk=pk, user=request.user)
    context = {'note': note}
    
    # Return as a plain HTML page that the browser can "Print to PDF"
    # This is more reliable than installing heavy PDF libs in a restricted environment
    return render(request, "dashboard/note_export.html", context)
