from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from main import models
from datetime import datetime
import json


@login_required(login_url="http://www.w3hacks.com/login")
def index(request):
    return render(request, "app/index.html")


@login_required(login_url="http://www.w3hacks.com/login")
def achievements(request):
    achievements = models.Achievement.objects.all()

    my_achievements = list(models.Profile.objects.get(user=request.user).achievements.all())

    return render(request, "app/achievements.html", context={
        "achievements": achievements,
        "my_achievements": my_achievements
    })


@login_required(login_url="http://www.w3hacks.com/login")
def leaderboards(request):
    all_profiles = models.Profile.objects.all()

    overall_rankings = sorted(all_profiles, key=lambda x: x.overall_ranking_points)
    project_rankings = sorted(all_profiles, key=lambda x: x.project_ranking_points)
    quiz_rankings = sorted(all_profiles, key=lambda x: x.quiz_ranking_points)
    exercise_rankings = sorted(all_profiles, key=lambda x: x.exercise_ranking_points)

    return render(request, "app/leaderboards.html", context={
        "overall_rankings": overall_rankings,
        "project_rankings": project_rankings,
        "quiz_rankings": quiz_rankings,
        "exercise_rankings": exercise_rankings
    })


# Activities views
@login_required(login_url="http://www.w3hacks.com/login")
def exercises(request):
    return render(request, "app/exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def project_exercises(request):
    topics = models.Topic.objects.all()
    project_exercises = models.ProjectExercise.objects.all()
    topic_object = None

    if request.GET.get("topic"):
        topic = request.GET.get("topic")

        # Iterating through project exercises to find ones that are in the topic
        iterable_project_exercises = project_exercises
        project_exercises = []
        for project_exercise in iterable_project_exercises:
            if project_exercise.topic.searchable_name == topic:
                project_exercises.append(project_exercise)

        # Topic object to pass into template
        topic_object = models.Topic.objects.get(searchable_name=topic)

    return render(request, "app/project-exercises.html", context={
        "topics": topics,
        "exercises": project_exercises,
        "topic": topic_object
    })


@login_required(login_url="http://www.w3hacks.com/login")
def project_exercise(request):
    # Receiving the submitted github link for the exercise
    if request.method == "POST":
        github_link = request.POST.get("github-link")
        print(github_link)

    project_id = request.GET.get("id")
    if project_id:
        if models.ProjectExercise.objects.filter(id=project_id).exists():
            project_exercise = models.ProjectExercise.objects.get(id=project_id)
        else:
            return HttpResponse("Invalid project exercise ID.")
    else:
        return HttpResponse("You must provide a project ID.")

    return render(request, "app/project-exercise.html", context={
        "exercise": project_exercise
    })


@login_required(login_url="http://www.w3hacks.com/login")
def quiz_exercises(request):
    topics = models.Topic.objects.all()
    quiz_exercises = models.QuizExercise.objects.all()
    topic_object = None

    if request.GET.get("topic"):
        topic = request.GET.get("topic")

        # Iterating through project exercises to find ones that are in the topic
        iterable_quiz_exercises = quiz_exercises
        quiz_exercises = []
        for quiz_exercise in iterable_quiz_exercises:
            if quiz_exercise.topic.searchable_name == topic:
                quiz_exercises.append(quiz_exercise)

        # Topic object to pass into template
        topic_object = models.Topic.objects.get(searchable_name=topic)

    return render(request, "app/quiz-exercises.html", context={
        "topics": topics,
        "exercises": quiz_exercises,
        "topic": topic_object
    })


@login_required(login_url="http://www.w3hacks.com/login")
def quiz_exercise(request):
    quiz_id = request.GET.get("id")
    if quiz_id:
        if models.QuizExercise.objects.filter(id=quiz_id).exists():
            quiz_exercise = models.QuizExercise.objects.get(id=quiz_id)
        else:
            return HttpResponse("Invalid quiz exercise ID.")
    else:
        return HttpResponse("You must provide a quiz ID.")

    return render(request, "app/quiz-exercise.html", context={
        "exercise": quiz_exercise
    })


@login_required(login_url="http://www.w3hacks.com/login")
def take_quiz(request):
    quiz_id = request.GET.get("id")
    if quiz_id:
        if models.QuizExercise.objects.filter(id=quiz_id).exists():
            quiz_exercise = models.QuizExercise.objects.get(id=quiz_id)
        else:
            return HttpResponse("Invalid quiz exercise ID.")
    else:
        return HttpResponse("You must provide a quiz ID.")

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


    return render(request, "app/take-quiz.html", context={
        "quiz": quiz_exercise,
        "questions": questions,
        "user_already_taken_quiz": user_already_taken_quiz
    })


@login_required(login_url="http://www.w3hacks.com/login")
def mini_exercises(request):
    topics = models.Topic.objects.all()
    mini_exercises = models.MiniExercise.objects.all()
    topic_object = None

    if request.GET.get("topic"):
        topic = request.GET.get("topic")

        # Iterating through project exercises to find ones that are in the topic
        iterable_mini_exercises = mini_exercises
        mini_exercises = []
        for mini_exercise in iterable_mini_exercises:
            if mini_exercise.topic.searchable_name == topic:
                mini_exercises.append(mini_exercise)

        # Topic object to pass into template
        topic_object = models.Topic.objects.get(searchable_name=topic)

    return render(request, "app/mini-exercises.html", context={
        "topics": topics,
        "exercises": mini_exercises,
        "topic": topic_object
    })


@login_required(login_url="http://www.w3hacks.com/login")
def mini_exercise(request):
    mini_id = request.GET.get("id")
    if mini_id:
        if models.MiniExercise.objects.filter(id=mini_id).exists():
            mini_exercise = models.MiniExercise.objects.get(id=mini_id)
        else:
            return HttpResponse("Invalid mini exercise ID.")
    else:
        return HttpResponse("You must provide a mini ID.")

    return render(request, "app/mini-exercise.html", context={
        "exercise": mini_exercise
    })


# Hackathon views
@login_required(login_url="http://www.w3hacks.com/login")
def hackathon(request):
    return render(request, "app/hackathon.html")


@login_required(login_url="http://www.w3hacks.com/login")
def about_the_hackathon(request):
    return render(request, "app/about-the-hackathon.html")


@login_required(login_url="http://www.w3hacks.com/login")
def past_hackathons(request):
    all_hackathons = models.Hackathon.objects.all()

    past_hackathons = []
    for hackathon in all_hackathons:
        # Hackathon end date was less than today
        if hackathon.end_datetime.strftime("%d/%m/%Y %H:%M:%S") < datetime.now().strftime("%d/%m/%Y %H:%M:%S"):
            past_hackathons.append(hackathon)

    return render(request, "app/past-hackathons.html", context={
        "past_hackathons": past_hackathons
    })


@login_required(login_url="http://www.w3hacks.com/login")
def future_hackathons(request):
    all_hackathons = models.Hackathon.objects.all()

    future_hackathons = []
    for hackathon in all_hackathons:
        # Hackathon end date was less than today
        if hackathon.start_datetime.strftime("%d/%m/%Y %H:%M:%S") > datetime.now().strftime("%d/%m/%Y %H:%M:%S"):
            future_hackathons.append(hackathon)

    return render(request, "app/future-hackathons.html", context={
        "future_hackathons": future_hackathons
    })


# Profile views
@login_required(login_url="http://www.w3hacks.com/login")
def profile(request, user_id):
    # Getting current user
    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
    else:
        return HttpResponse("User does not exist.")

    # Getting profile from current user
    profile = models.Profile.objects.get(user=user)

    return render(request, "app/profile.html", context={
        "profile": profile
    })


@login_required(login_url="http://www.w3hacks.com/login")
def edit_profile(request, user_id):
    # Getting current user
    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
    else:
        return HttpResponse("User does not exist.")

    # Getting profile from current user
    profile = models.Profile.objects.get(user=user)

    # Checking to see if current user is the one editing profile
    if user == request.user:
        pass
    else:
        return HttpResponse("You do not have permission to modify this profile.")

    if request.method == "POST":
        # Grabbing all pieces of form POST data
        # Grabbing default Django User data
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Grabbing custom profile data
        biography = request.POST.get("biography")
        birthday = request.POST.get("birthday")
        education = request.POST.get("education")
        skills = request.POST.get("skills").split(",")

        # Social Links
        github_profile = request.POST.get("github-profile")
        linkedin_profile = request.POST.get("linkedin-profile")
        twitter_profile = request.POST.get("twitter-profile")
        instagram_profile = request.POST.get("instagram-profile")
        facebook_profile = request.POST.get("facebook-profile")
        twitch_profile = request.POST.get("twitch-profile")
        personal_website = request.POST.get("personal-website")

        # Updating user
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username


        # Updating profile
        profile = models.Profile.objects.get(user=request.user)
        profile.biography = biography
        profile.education = education
        profile.skills = skills
        profile.github_profile = github_profile
        profile.linkedin_profile = linkedin_profile
        profile.twitter_profile = twitter_profile
        profile.instagram_profile = instagram_profile
        profile.facebook_profile = facebook_profile
        profile.twitch_profile = twitch_profile
        profile.personal_website = personal_website

        # Checking if they provided picture
        if 'profile-picture' in request.FILES:
            profile.profile_picture = request.FILES['profile-picture']

        user.save()
        profile.save()

        return HttpResponseRedirect("/profile/" + str(user.id))


    return render(request, "app/edit-profile.html", context={
        "profile": profile
    })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("http://w3hacks.com")



# API VIEWS
@csrf_exempt
def create_completed_quiz_exercise(request):
    if request.method == "POST":
        data = json.loads(request.body)
        quiz_exercise_id = data["quiz_exercise_id"]
        quiz_exercise = models.QuizExercise.objects.get(id=quiz_exercise_id)
        answers = data["answers"]

        # Creating completed quiz exercise
        completed_quiz_exercise = models.CompletedQuizExercise(quiz_exercise=quiz_exercise, answers=answers)
        completed_quiz_exercise.save()

        # Adding completed quiz exercise to user profile
        profile = request.user.profile
        profile.completed_quiz_exercises.add(completed_quiz_exercise)
        profile.save()

        return HttpResponse("hi")
