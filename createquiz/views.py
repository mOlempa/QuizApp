from django.shortcuts import render, get_object_or_404, redirect
from .forms import QuizForm, QuestionForm, AnswerFormSet
from uploader.models import Quiz, Question, Answer


def index(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        print("HERE!!")
        if form.is_valid():
            quiz = form.save()
            print("----------------> quiz.id :")
            print(quiz.id)
            return redirect("add_question", quiz.id)
    else:
        form = QuizForm()

    return render(request, 'createquiz/index.html', {
        'form': form
    })


def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = AnswerFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            quiz.save()

            # Save the question but don't commit to DB yet
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            
            # Save the answers linked to that question
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()

            # If user wants to add another question to the quiz
            if 'save_and_add' in request.POST:
                return redirect("add_question", quiz.id)
            # iF user wants to complete creating the quiz
            elif 'save_and_exit' in request.POST:
                questions = Question.objects.filter(quiz_id=quiz.id)
                answers = Answer.objects.filter(question__in=questions)
                context = {'quiz': quiz, 'questions': questions, 'answers': answers}
                return render(request, 'quizlist/view_quiz.html', context)
            else:
                quizzes = Quiz.objects.order_by('name')
                context = {'quizzes': quizzes}
                return render(request, 'quizlist/index.html', context)
    else:
        form = QuestionForm()
        formset = AnswerFormSet()
        return render(request, 'createquiz/create.html', {
            'form': form,
            'formset': formset,
            'quiz': quiz
        })