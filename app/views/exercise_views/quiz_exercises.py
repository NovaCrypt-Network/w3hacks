from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import models
import json


@login_required(login_url="/login/")
def quiz_exercises(request):
    quiz_exercises = models.QuizExercise.objects.all()
    specific_topic = None

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Quiz Exercises", "link": "/exercises/quiz-exercises/" }
    ]

    return render(request, "app/exercises/quiz-exercises/quiz-exercises.html", context={
        "exercises": quiz_exercises,
        "topic": specific_topic,
        "breadcrumbs": breadcrumbs
    })


@login_required(login_url="/login/")
def quiz_exercise(request):
    quiz_id = request.GET.get("id")
    if quiz_id:
        if models.QuizExercise.objects.filter(id=quiz_id).exists():
            quiz_exercise = models.QuizExercise.objects.get(id=quiz_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Quiz Exercises", "link": "/exercises/quiz-exercises/" },
        { "text": quiz_exercise.name, "link": None }
    ]

    # Checking to see if user already took this quiz
    user_already_taken_quiz = False
    for completed_quiz_exercise in list(request.user.profile.completed_quiz_exercises.all()):
        if completed_quiz_exercise.quiz_exercise == quiz_exercise:
            user_already_taken_quiz = True

    return render(request, "app/exercises/quiz-exercises/quiz-exercise.html", context={
        "exercise": quiz_exercise,
        "resources": list(quiz_exercise.resources.all()),
        "breadcrumbs": breadcrumbs,
        "user_already_taken_quiz": user_already_taken_quiz
    })


@login_required(login_url="/login/")
def take_quiz(request):
    quiz_id = request.GET.get("id")
    if quiz_id:
        if models.QuizExercise.objects.filter(id=quiz_id).exists():
            quiz_exercise = models.QuizExercise.objects.get(id=quiz_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Quiz Exercises", "link": "/exercises/quiz-exercises/" },
        { "text": quiz_exercise.name, "link": "/exercises/quiz-exercises/exercise/?id=" + quiz_exercise.id },
        { "text": "Take Quiz", "link": None }
    ]

    # Formatting questions with question and answers
    questions = []
    for question in list(quiz_exercise.questions.all()):
        questions.append({
            "question": question.question,
            "answers": question.answers
        })

    questions = json.dumps(questions)

    # Checking to see if user already took this quiz
    user_already_taken_quiz = False
    for completed_quiz_exercise in list(request.user.profile.completed_quiz_exercises.all()):
        if completed_quiz_exercise.quiz_exercise == quiz_exercise:
            user_already_taken_quiz = True


    return render(request, "app/exercises/quiz-exercises/take-quiz.html", context={
        "quiz": quiz_exercise,
        "breadcrumbs": breadcrumbs,
        "questions": questions,
        "user_already_taken_quiz": user_already_taken_quiz
    })


@login_required(login_url="/login/")
def quiz_results(request):
    # Grabbing quiz from query parameters
    quiz_id = request.GET.get("id")
    if quiz_id:
        if models.QuizExercise.objects.filter(id=quiz_id).exists():
            quiz_exercise = models.QuizExercise.objects.get(id=quiz_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Quiz Exercises", "link": "/exercises/quiz-exercises/" },
        { "text": quiz_exercise.name, "link": "/exercises/quiz-exercises/exercise/?id=" + quiz_exercise.id },
        { "text": "Quiz Results", "link": None }
    ]

    # Grabbing completed quiz exercise
    if models.CompletedQuizExercise.objects.filter(quiz_exercise=quiz_exercise).exists():
        for completed_exercise in models.CompletedQuizExercise.objects.filter(quiz_exercise=quiz_exercise):
            if completed_exercise in list(request.user.profile.completed_quiz_exercises.all()):
                completed_quiz_exercise = completed_exercise
    else:
        return HttpResponse("You haven't completed this quiz yet.")

    # Organizing questions and answers for easy access
    quiz_questions = list(quiz_exercise.questions.all())
    user_answers = completed_quiz_exercise.answers
    results = []
    for i in range(len(quiz_questions)):
        result = {}
        current_question = quiz_questions[i]

        result["got_this_correct"] = (current_question.answers[current_question.correct_answer_index] == user_answers[i])
        result["question"] = current_question.question
        result["answers"] = current_question.answers
        result["correct_answer"] = current_question.answers[current_question.correct_answer_index]
        result["user_answer"] = user_answers[i]

        results.append(result)

    # results = json.dumps(results)

    return render(request, "app/exercises/quiz-exercises/quiz-results.html", context={
        "quiz_exercise": quiz_exercise,
        "completed_quiz_exercise": completed_quiz_exercise,
        "breadcrumbs": breadcrumbs,
        "results": results
    })
