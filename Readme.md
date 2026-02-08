# MyQuiz Application Documentation

## Table of Contents
1. [Installation & Setup](#installation--setup)
2. [Starting the Application](#starting-the-application)
3. [User Guide](#user-guide)
4. [Admin Guide](#admin-guide)
5. [API Documentation](#api-documentation)
6. [File Upload Format](#file-upload-format)
7. [Troubleshooting](#troubleshooting)

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd myquiz
```

### Step 2: Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Required Packages
```bash
# Install Django and dependencies
pip install django==5.2.11
pip install mysqlclient

# Alternative if mysqlclient fails:
pip install pymysql
```

### Step 4: Database Configuration

**Option A: Use Existing Database (as configured)**
The application is currently configured to connect to:
- Host: `s169.cyber-folks.pl`
- Database: `magole_calendar`
- User: `magole_moss`
- Port: `3306`

**Option B: Configure Your Own Database**
1. Create a MySQL database:
```sql
CREATE DATABASE myquiz_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'myquiz_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON myquiz_db.* TO 'myquiz_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Update `myquiz/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myquiz_db',
        'USER': 'myquiz_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

### Step 5: Run Migrations
```bash
# Apply database migrations
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser
```

### Step 6: Collect Static Files
```bash
python manage.py collectstatic
```

---

## Starting the Application

### Development Server
```bash
# Make sure virtual environment is activated
# venv\Scripts\activate (Windows) or source venv/bin/activate (macOS/Linux)

# Start the Django development server
python manage.py runserver

# Server will start at http://127.0.0.1:8000/
```

### Access Points
- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Login**: http://127.0.0.1:8000/login/
- **Registration**: http://127.0.0.1:8000/registration/

---

## User Guide

### Registration & Login

#### Creating an Account
1. Navigate to http://127.0.0.1:8000/registration/
2. Enter a username
3. Enter a password (twice for confirmation)
4. Click "Register"
5. You will be automatically logged in and redirected to the home page

#### Logging In
1. Navigate to http://127.0.0.1:8000/login/
2. Enter your username and password
3. Click "Login"

#### Logging Out
- Click the "Log out" button in the navigation bar

### Taking Quizzes

#### Browse Available Quizzes
1. Click "Do Quizzes" in the navigation bar
2. You'll see a list of all available quizzes
3. Click "DO" next to any quiz to start

#### Taking a Quiz
1. Read each question carefully
2. Check the boxes for answers you believe are correct
3. Multiple answers may be correct for a single question
4. Click "Check" to submit your answers

#### Viewing Results
- Correct answers are shown in **green**
- Incorrect answers are shown in **red**
- Your selected answers will have checkboxes checked
- Click "Back to list" to return to the quiz list

### Creating Quizzes (Authenticated Users Only)

#### Method 1: Manual Creation

**Step 1: Create Quiz**
1. Click "Create" in the navigation bar
2. Enter a name for your quiz
3. Click "CREATE NEW"

**Step 2: Add Questions**
1. Enter the question text
2. Add at least one answer:
   - Enter answer text
   - Check "Is correct" for correct answers
3. Click "Add Another Answer" to add more answer options
4. Choose what to do next:
   - **"Add New Question"**: Save this question and add another
   - **"Finish Quiz Creation"**: Save and view the completed quiz

#### Method 2: File Upload

**Step 1: Prepare Quiz File**
Create a `.txt` file following this format:
```
Question text here?
(T) Correct answer
(F) Incorrect answer
(F) Another incorrect answer
#
Next question here?
(T) This is correct
(F) This is incorrect
```

See [File Upload Format](#file-upload-format) for details.

**Step 2: Upload File**
1. Click "Upload" in the navigation bar
2. Click "Choose File" and select your `.txt` file
3. Click "Upload and Show"
4. The quiz will be automatically created with all questions and answers

### Managing Your Quizzes

#### View Your Quizzes
1. Click "My Quizzes" in the navigation bar
2. You'll see all quizzes you've created

#### View Quiz Details
1. In "My Quizzes", click "VIEW" next to a quiz
2. You'll see all questions and answers for that quiz

#### Edit Questions
1. View the quiz details
2. Click "Edit Question" next to the question you want to modify
3. Update the question text or answers
4. Add or remove answer options
5. Click "Save Question"

#### Add More Questions
1. View the quiz details
2. Click "Add question" at the bottom
3. Follow the same process as creating a new question

#### Delete Questions
1. View the quiz details
2. Click "Delete Question" next to the question to remove
3. The question and all its answers will be deleted

#### Delete Entire Quiz
1. In "My Quizzes", click "DELETE" next to the quiz
2. The quiz and all associated questions/answers will be permanently deleted

---

## Admin Guide

### Accessing Admin Panel
1. Navigate to http://127.0.0.1:8000/admin/
2. Log in with superuser credentials
3. You have access to all Django models and database entries

### Admin Capabilities

#### Quiz Management
Superusers have special privileges:
- **View All Quizzes**: See quizzes from all users (not just their own)
- **Edit Any Quiz**: Modify questions and answers in any quiz
- **Delete Any Quiz**: Remove any quiz from the system

#### Database Access
From the admin panel, you can:
- View all Quiz objects
- View all Question objects
- View all Answer objects
- Perform bulk operations
- Export data

### Admin-Specific Features

#### Viewing All Quizzes
When a superuser accesses "My Quizzes", they see ALL quizzes in the system, not just their own.

#### Permission Checks
The application includes permission checks:
- Regular users can only edit/delete their own quizzes
- Superusers can edit/delete any quiz
- Attempting unauthorized actions raises a `PermissionDenied` error

---

## API Documentation

### URL Structure

#### Root URLs (`myquiz/urls.py`)
| URL Pattern | View | Name | Description |
|------------|------|------|-------------|
| `/admin/` | `admin.site.urls` | - | Django admin panel |
| `/` | `include('uploader.urls')` | - | Home and upload functionality |
| `/quizlist/` | `include('quizlist.urls')` | - | Quiz management |
| `/quiztaking/` | `include('quiztaking.urls')` | - | Quiz taking functionality |
| `/createquiz/` | `include('createquiz.urls')` | - | Quiz creation |
| `/registration/` | `include('registration.urls')` | - | User registration |
| `/logout/` | `LogoutView.as_view()` | `logout` | User logout |
| `/login/` | `LoginView.as_view()` | `login` | User login |

### Uploader App (`uploader/urls.py`)

#### Home Page
- **URL**: `/`
- **View**: `index`
- **Name**: `uploader`
- **Method**: GET
- **Description**: Displays the home page
- **Authentication**: Not required

#### File Upload
- **URL**: `/upload/`
- **View**: `upload_file_view`
- **Name**: `upload_file`
- **Methods**: GET, POST
- **Description**: Upload quiz file and parse into database
- **Authentication**: Not required (should be @login_required)
- **POST Parameters**:
  - `text_file`: File upload (.txt format)
- **Response**: Renders uploaded file content and creates quiz

### Quiz List App (`quizlist/urls.py`)

#### List User's Quizzes
- **URL**: `/quizlist/`
- **View**: `index`
- **Name**: `quizlist`
- **Method**: GET
- **Description**: Lists quizzes owned by current user (or all if superuser)
- **Authentication**: Not required (filters by user if authenticated)

#### View Quiz Details
- **URL**: `/quizlist/<int:id>/`
- **View**: `get`
- **Name**: `get`
- **Method**: GET
- **Description**: View all questions and answers for a specific quiz
- **Parameters**:
  - `id`: Quiz ID
- **Authentication**: Not required

#### List All Quizzes (Public)
- **URL**: `/quizlist/all_quizzes/`
- **View**: `get_all`
- **Name**: `all_quizzes`
- **Method**: GET
- **Description**: Lists all quizzes available for taking
- **Authentication**: Not required

#### Delete Quiz
- **URL**: `/quizlist/<int:id>/remove/`
- **View**: `remove`
- **Name**: `remove`
- **Method**: GET
- **Description**: Deletes a quiz (owner or superuser only)
- **Parameters**:
  - `id`: Quiz ID
- **Authentication**: Required
- **Permissions**: Owner or superuser

#### Edit Question
- **URL**: `/quizlist/<int:id>/edit/`
- **View**: `edit`
- **Name**: `edit`
- **Methods**: GET, POST
- **Description**: Edit a question and its answers
- **Parameters**:
  - `id`: Question ID
- **Authentication**: Required
- **Permissions**: Owner or superuser
- **POST Data**: QuestionForm and AnswerFormSet

#### Delete Question
- **URL**: `/quizlist/<int:id>/remove_question/`
- **View**: `remove_question`
- **Name**: `remove_question`
- **Method**: GET
- **Description**: Deletes a question and its answers
- **Parameters**:
  - `id`: Question ID
- **Authentication**: Required (decorator)
- **Permissions**: Owner or superuser

### Quiz Taking App (`quiztaking/urls.py`)

#### Take Quiz
- **URL**: `/quiztaking/<int:id>/`
- **View**: `index`
- **Name**: `quiztaking`
- **Methods**: GET, POST
- **Description**: Display quiz for taking or process submitted answers
- **Parameters**:
  - `id`: Quiz ID
- **GET**: Displays quiz form
- **POST Parameters**:
  - `selected_answers`: List of answer IDs (checkboxes)
- **POST Response**: Shows results with correct/incorrect highlighting

### Create Quiz App (`createquiz/urls.py`)

#### Create New Quiz
- **URL**: `/createquiz/`
- **View**: `index`
- **Name**: `createquiz`
- **Methods**: GET, POST
- **Description**: Create a new quiz
- **Authentication**: Not required (should be @login_required)
- **POST Data**: QuizForm (quiz name)
- **Redirect**: To add_question view

#### Add Question to Quiz
- **URL**: `/createquiz/<int:quiz_id>/`
- **View**: `add_question`
- **Name**: `add_question`
- **Methods**: GET, POST
- **Description**: Add questions and answers to a quiz
- **Parameters**:
  - `quiz_id`: Quiz ID
- **Authentication**: Required (decorator)
- **POST Data**: 
  - QuestionForm
  - AnswerFormSet
- **POST Buttons**:
  - `save_and_add`: Redirects to add another question
  - `save_and_exit`: Shows completed quiz
  - Default: Returns to quiz list

### Registration App (`registration/urls.py`)

#### User Registration
- **URL**: `/registration/`
- **View**: `register`
- **Name**: `registration`
- **Methods**: GET, POST
- **Description**: User registration form
- **POST Data**: UserCreationForm
- **Success**: Auto-login and redirect to home

### Models

#### Quiz Model
```python
class Quiz(models.Model):
    owner = ForeignKey(User, on_delete=RESTRICT, default=2)
    name = CharField(max_length=200)
```

**Fields**:
- `id`: Auto-generated primary key
- `owner`: Foreign key to User model
- `name`: Quiz name (max 200 characters)

**Relationships**:
- One-to-many with Question (related_name='questions')
- One-to-many with User (related_name='quizzes')

#### Question Model
```python
class Question(models.Model):
    text = TextField()
    quiz = ForeignKey(Quiz, on_delete=CASCADE)
```

**Fields**:
- `id`: Auto-generated primary key
- `text`: Question text (no length limit)
- `quiz`: Foreign key to Quiz

**Relationships**:
- Many-to-one with Quiz (related_name='questions')
- One-to-many with Answer (related_name='answers')

**Cascade Delete**: Deleting a quiz deletes all its questions

#### Answer Model
```python
class Answer(models.Model):
    question = ForeignKey(Question, on_delete=CASCADE)
    text = CharField(max_length=255)
    is_correct = BooleanField(default=False)
```

**Fields**:
- `id`: Auto-generated primary key
- `question`: Foreign key to Question
- `text`: Answer text (max 255 characters)
- `is_correct`: Boolean flag for correct answers

**Relationships**:
- Many-to-one with Question (related_name='answers')

**Cascade Delete**: Deleting a question deletes all its answers

---

## File Upload Format

### Text File Structure

Quiz files must be plain text (`.txt`) with the following format:

```
Question text here?
(T) Correct answer
(F) Incorrect answer
(F) Another incorrect answer
#
Next question text?
(T) Correct answer one
(T) Correct answer two
(F) Incorrect answer
#
Third question?
(T) Only correct answer
(F) Wrong answer
(F) Also wrong
(F) Still wrong
```

### Format Rules

1. **Question Line**: First line of each block (no prefix required)
2. **Answer Lines**: Following lines prefixed with:
   - `(T)` - True/Correct answer
   - `(F)` - False/Incorrect answer
3. **Question Separator**: Use `#` on its own line between questions
4. **Whitespace**: Leading/trailing spaces are automatically trimmed
5. **File Name**: Used as the quiz name (without .txt extension)

### Example Files

**Example 1: Simple Quiz** (`test.txt`)
```
What is this app for?
(F) Making new friends
(F) Looking up cat memes
(T) Creating fantastic quizzes yay
#
Are wolves cats?
(F) Yes, obviously
(T) Dude, no
(F) I don't understand the question
```

**Example 2: Multiple Correct Answers**
```
Which are programming languages?
(T) Python
(T) JavaScript
(F) HTML
(T) Java
(F) CSS
#
What is 2+2?
(F) 3
(T) 4
(F) 5
(F) 22
```

### Upload Process

1. File is uploaded via `/upload/`
2. `parse_and_save_questions()` function processes the file:
   - Splits content on `#` character
   - Creates Quiz object with filename (minus extension)
   - Creates Question objects for each block
   - Creates Answer objects with correct `is_correct` flags
3. All database operations wrapped in transaction for safety
4. File content displayed on page after upload

---

## Troubleshooting

#### Permission Denied Errors
- Ensure you're logged in
- Check if you're the quiz owner
- Verify superuser status for admin actions

#### File Upload Not Working
- Check file format (must be .txt)
- Verify format follows specification
- Check for special characters or encoding issues
- Look at console output for parsing errors

### Debug Mode

For development, DEBUG mode is enabled in `settings.py`:
```python
DEBUG = True
```

**Important**: Set `DEBUG = False` for production and configure `ALLOWED_HOSTS`

### Logging

Add print statements or use Django logging to debug:
```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```
---

## Version Information

- **Django**: 5.2.11
- **Python**: 3.8+
- **MySQL**: 5.7+ or 8.0+
- **Database Driver**: mysqlclient

---

## License & Credits

This is an educational project for learning Django web development.

**Project Structure**:
- `uploader`: Home page and file upload functionality
- `quizlist`: Quiz viewing and management
- `quiztaking`: Quiz taking and scoring
- `createquiz`: Manual quiz creation
- `registration`: User registration system

---

*Last Updated: February 2026*
