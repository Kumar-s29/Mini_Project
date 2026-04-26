from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["title", "description"]


class DateInput(forms.DateInput):
    input_type = "date"


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {"due": DateInput()}
        fields = ["subject", "title", "description", "due", "is_finished"]


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter Your Search :")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "is_finished"]


class ConversionForm(forms.Form):
    CHOICES = [("length", "Length"), ("mass", "Mass")]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class ConversionLengthForm(forms.Form):
    CHOICES = [("yard", "Yard"), ("foot", "Foot")]
    input = forms.CharField(
        required=False,
        label="Value",
        widget=forms.TextInput(
            attrs={"type": "number", "placeholder": "Enter the number"}
        ),
    )
    measure1 = forms.ChoiceField(label="From", choices=CHOICES, widget=forms.Select)
    measure2 = forms.ChoiceField(label="To", choices=CHOICES, widget=forms.Select)


class ConversionMassForm(forms.Form):
    CHOICES = [("pound", "Pound"), ("kilogram", "Kilogram")]
    input = forms.CharField(
        required=False,
        label="Value",
        widget=forms.TextInput(
            attrs={"type": "number", "placeholder": "Enter the number"}
        ),
    )
    measure1 = forms.ChoiceField(label="From", choices=CHOICES, widget=forms.Select)
    measure2 = forms.ChoiceField(label="To", choices=CHOICES, widget=forms.Select)


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["subject", "marks_obtained", "total_marks"]

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        widgets = {"date": DateInput()}
        fields = ["subject", "title", "date", "importance"]

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }
        fields = ["day", "subject", "start_time", "end_time", "room"]

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ["subject", "question", "answer"]

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email"]
