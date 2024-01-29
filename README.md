QuizGPT uses OpenAI's GPT models to create and grade quizzes on topics of your choice.

## CLI
```shell
# Set-up
$ cd cli
$ pip install -r requirements.txt
$ export OPENAI_API_KEY=..
$ alias quizgpt='python main.py'

# Import a quiz
$ quizgpt import samples/postwar-us-history.json
$ quizgpt list
     1  Post-war United States history                      (5 questions)

# Take a quiz
$ quizgpt take

# Create your own subject
$ quizgpt create
# Add questions
$ quizgpt add
```

## Web interface
*The web interface is under development and not yet completely functional.*

To run the backend server:

```shell
$ cd backend
$ source .venv/bin/activate
$ export OPENAI_API_KEY=...
$ uvicorn main:app --reload --port 5757
```

To serve the frontend:

```shell
$ cd frontend
$ npm run dev
```

To install the project:

```shell
$ cd backend
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cd ../frontend
$ npm install
```

The project is developed with Python 3.11 and Node 20.8. Older versions may not work.
