from django.shortcuts import render, get_object_or_404
from uploader.models import Quiz, Question, Answer

# Create your views here.
def index(request):
    quizzes = Quiz.objects.order_by('name')
    # Create a dictionary storing database elements under quizzes variable
    context = {'quizzes': quizzes}
    # Sending rendered site together with database elements, which are used in quizlist/index.html file
    return render(request, 'quizlist/index.html', context)

def get(request, id):
    # funkcja get_object_or_404 zwraca element z bazy
    # danych o danej warto±ci argumentu
    # lub przesªyªa do kilenta bª¡d
    quiz = get_object_or_404(Quiz, id=id)
    questions = Question.objects.filter(quiz_id=quiz.id)
    answers = Answer.objects.filter(question__in=questions)
    context = {'quiz': quiz, 'questions': questions, 'answers': answers}
    return render(request, 'quizlist/view_quiz.html', context)