from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from .models import Question, Answer, Quiz

# Create your views here.
def index(request):
    #return HttpResponse("To jest pierwsza aplikacja")
    return render(request, 'index.html')

def upload_file_view(request):
    file_content = None  # Initialize as None
    filename = None

    if request.method == 'POST' and request.FILES.get('text_file'):
        uploaded_file = request.FILES['text_file']
        
        # Read and decode the content
        file_content = uploaded_file.read().decode('utf-8')
        filename = uploaded_file.name

        # Wrap in a transaction for safety
        try:
            with transaction.atomic():
                quiz_object = Quiz.objects.create(name=filename.replace('.txt', ''), owner=request.user)
                parse_and_save_questions(file_content, quiz_object)
        except Exception as e:
            # Handle parsing errors (e.g., wrong format)
            print(f"Error processing file: {e}")

    # Pass 'file_content' to the template context
    return render(request, 'upload.html', {
        'content': file_content,
        'filename': filename
    })
    

def parse_and_save_questions(file_content, quiz_object):
    # Split the file into blocks based on an empty line with #
    # .strip() removes leading/trailing whitespace; split('#') finds # and splits
    blocks = file_content.strip().split('#')

    for block in blocks:
        print("------------------BLOCK --------------------")
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        if not lines:
            continue

        # The first line is always the question
        question_text = lines[0]
        question_obj = Question.objects.create(text=question_text, quiz=quiz_object)

        # The remaining lines are answers
        for answer_line in lines[1:]:
            is_correct = False
            clean_answer = answer_line

            if answer_line.startswith('(T)'):
                is_correct = True
                clean_answer = answer_line.replace('(T)', '', 1).strip()
            elif answer_line.startswith('(F)'):
                is_correct = False
                clean_answer = answer_line.replace('(F)', '', 1).strip()

            Answer.objects.create(
                question=question_obj,
                text=clean_answer,
                is_correct=is_correct
            )