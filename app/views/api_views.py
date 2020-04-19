from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from main import models
import json


@csrf_exempt
def create_completed_quiz_exercise(request):
    if request.method == "POST":
        data = json.loads(request.body) # Grabbing post data

        # Grabbing quiz exercise from ID
        quiz_exercise_id = data["quiz_exercise_id"]
        quiz_exercise = models.QuizExercise.objects.get(id=quiz_exercise_id)
        questions = list(quiz_exercise.questions.all())

        # Grabbing answers
        user_answers = data["userAnswers"]

        # Grabbing length of questions
        number_of_questions = len(questions)

        # Determining number of correct answers
        number_of_correct_answers = 0
        print(range(len(questions)))
        for i in range(len(questions)):
            question = questions[i].question # Grabbing question
            answers = questions[i].answers # Grabbing question answers
            correct_answer = answers[questions[i].correct_answer_index]
            user_answer = user_answers[i] # Grabbing user's answer

            # Determining if the answer is correct
            if correct_answer == user_answer:
                 number_of_correct_answers += 1


        # Creating completed quiz exercise
        completed_quiz_exercise = models.CompletedQuizExercise(quiz_exercise=quiz_exercise, answers=user_answers, number_of_questions=number_of_questions, number_of_correct_answers=number_of_correct_answers)
        completed_quiz_exercise.save()

        # Adding completed quiz exercise to user profile
        profile = request.user.profile
        profile.completed_quiz_exercises.add(completed_quiz_exercise)
        profile.save()

        return HttpResponse("Created CompletedQuizExercise object.")
