from django.shortcuts import render, get_object_or_404, redirect
from uploader.models import Quiz, Question, Answer

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

# def edit(request, id):
#     question = get_object_or_404(Question, id=id)
#     # If POST - get filled form data
#     # If GET - send an empty form
#     if request.method == 'POST':
#         # Check if form is valid
#         form = QuestionForm(request.POST, instance=question)
#         if form.is_valid():
#             # If data is valid, add to database
#             form = form.save(commit=False)
#             form.author = request.user.username
#             form.create_time = timezone.now()
#             form.last_edit_time = timezone.now()
#             form.save()
#             return redirect('view_todo')
#         # If data is not valid, send the form back to the client (errors will be marked automatically)
#         else:
#             context = {'form': form}
#             return render(request, 'todo/edit.html', context)
#     else:
#         form = TodoForm(instance=todo)
#         context = {'form': form, 'id': id}
#         return render(request, 'todo/edit.html', context)


def remove(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    quiz.delete()
    return redirect('quizlist')