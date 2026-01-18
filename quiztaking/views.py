from django.shortcuts import render, get_object_or_404
from uploader.models import Question, Answer, Quiz
from django.http import HttpResponse

# Create your views here.
def index(request, id):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_answers')
        chosen_answers = Answer.objects.filter(id__in=selected_ids)
        for a in chosen_answers:
            print("Chosen answer: "+ a.text)
        return HttpResponse("You solved the quiz, yay")
    else:
        quiz = get_object_or_404(Quiz, id=id)
        questions = Question.objects.filter(quiz_id=quiz.id)
        answers = Answer.objects.filter(question__in=questions)
        context = {'quiz': quiz, 'questions': questions, 'answers': answers}
        return render(request, 'quiztaking/index.html', context)

        