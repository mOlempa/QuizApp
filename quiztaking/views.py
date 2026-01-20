from django.shortcuts import render, get_object_or_404
from uploader.models import Question, Answer, Quiz
from django.http import HttpResponse

# Create your views here.
def index(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    questions = Question.objects.filter(quiz_id=quiz.id)
    answers = Answer.objects.filter(question__in=questions)
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_answers')
        chosen_answers = Answer.objects.filter(id__in=selected_ids)
        correct_answers = []
        for a in answers:
            if a.is_correct and a in chosen_answers:
                print("Correct answer: "+ a.text + " (True)")
                correct_answers.append(a.id)
            if not a.is_correct and a not in chosen_answers:
                print("Correct answer: "+ a.text + " (False)")
                correct_answers.append(a.id)
            #print("Chosen answer: "+ a.text)
        #return HttpResponse("You solved the quiz, yay")
        context = {'quiz': quiz, 
                   'questions': questions, 
                   'answers': answers, 
                   'chosen_answers': chosen_answers, 
                   'correct_answers': correct_answers}
        #print("Correct answers list:")
        #print(correct_answers)
        return render(request, 'quiztaking/solved.html', context)
    else:
        context = {'quiz': quiz, 'questions': questions, 'answers': answers}
        return render(request, 'quiztaking/index.html', context)

        