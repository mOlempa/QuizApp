from django.shortcuts import render, get_object_or_404, redirect
from uploader.models import Quiz, Question, Answer
from createquiz.forms import QuestionForm, AnswerFormSet

# Create your views here.
def index(request):
    quizzes = Quiz.objects.order_by('name')
    # Create a dictionary storing database elements under quizzes variable
    context = {'quizzes': quizzes}
    # Sending rendered site together with database elements, which are used in quizlist/index.html file
    return render(request, 'quizlist/index.html', context)

def get(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    questions = Question.objects.filter(quiz_id=quiz.id)
    answers = Answer.objects.filter(question__in=questions)
    context = {'quiz': quiz, 'questions': questions, 'answers': answers}
    return render(request, 'quizlist/view_quiz.html', context)

def edit(request, id):
    question = get_object_or_404(Question, id=id)
    quiz = get_object_or_404(Quiz, id=question.quiz.id)
    
    if request.method == "POST":
        # Pass instance=question so Django knows we are updating, not creating
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save() # This saves all answers and deletes those marked for deletion

            # Redirect logic
            questions = Question.objects.filter(quiz_id=quiz.id)
            answers = Answer.objects.filter(question__in=questions)
            context = {'quiz': quiz, 'questions': questions, 'answers': answers}
            return render(request, 'quizlist/view_quiz.html', context)
    else:
        # Prefill the question text
        form = QuestionForm(instance=question)
        # Prefill the formset with existing answers related to this question
        formset = AnswerFormSet(instance=question)

    return render(request, 'quizlist/edit.html', {
        'form': form,
        'formset': formset,
        'quiz': quiz
    })


def remove(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    quiz.delete()
    return redirect('quizlist')


# def remove_question(request, id):
#     question = get_object_or_404(Question, id=id)
#     quiz = Quiz.objects.filter(id=question.quiz.id)
#     question.delete()
#     questions = Question.object.filter(quiz_id=quiz.id)
#     answers = Answer.objects.filter(question__in=questions)
#     context = {'quiz': quiz, 'questions': questions, 'answers': answers}
#     return render(request, 'quizlist/view_quiz.html', context)