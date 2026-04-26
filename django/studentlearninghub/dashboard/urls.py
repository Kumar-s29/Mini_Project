from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("notes", views.notes, name="notes"),
    path("delete_note/<int:pk>", views.delete_note, name="delete-note"),
    path("notes_detail/<int:pk>", views.NotesDetailView.as_view(), name="notes-detail"),
    path("homework", views.homework, name="homework"),
    path("update_homework/<int:pk>", views.update_homework, name="update-homework"),
    path("delete_homework/<int:pk>", views.delete_homework, name="delete-homework"),
    path("youtube", views.youtube, name="youtube"),
    path("todo", views.todo, name="todo"),
    path("update_todo/<int:pk>", views.update_todo, name="update-todo"),
    path("delete-todo/<int:pk>", views.delete_todo, name="delete-todo"),
    path("books", views.books, name="books"),
    path("dictionary", views.dictionary, name="dictionary"),
    path("wiki", views.wiki, name="wiki"),
    path("conversion", views.conversion, name="conversion"),
    
    # New Features
    path("grades", views.grades, name="grades"),
    path("delete_grade/<int:pk>", views.delete_grade, name="delete-grade"),
    path("exams", views.exams, name="exams"),
    path("delete_exam/<int:pk>", views.delete_exam, name="delete-exam"),
    path("timetable", views.timetable, name="timetable"),
    path("delete_timetable/<int:pk>", views.delete_timetable, name="delete-timetable"),
    path("flashcards", views.flashcards, name="flashcards"),
    path("delete_flashcard/<int:pk>", views.delete_flashcard, name="delete-flashcard"),
    path("analytics", views.analytics, name="analytics"),
    path("focus", views.focus_timer, name="focus"),
    path("whiteboard", views.whiteboard, name="whiteboard"),
    path("ai_assistant", views.ai_assistant, name="ai-assistant"),
    path("export_note/<int:pk>", views.export_note_pdf, name="export-note"),
]
