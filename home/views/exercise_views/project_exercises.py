from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from main import models


@login_required(login_url="/login/")
def project_exercises(request):
    project_exercises = models.ProjectExercise.objects.all()
    specific_topic = None

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Project Exercises", "link": "/exercises/project-exercises/" }
    ]


    return render(request, "home/exercises/project-exercises/project-exercises.html", context={
        "exercises": project_exercises,
        "topic": specific_topic,
        "breadcrumbs": breadcrumbs
    })


@login_required(login_url="/login/")
def project_exercise(request):
    message = None
    project_id = request.GET.get("id")
    if project_id:
        if models.ProjectExercise.objects.filter(id=project_id).exists():
            project_exercise = models.ProjectExercise.objects.get(id=project_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")


    # Grabbing topic for breadcrumbs
    topic = project_exercise.topic

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Project Exercises", "link": "/exercises/project-exercises/" },
        { "text": topic.name, "link": "/exercises/project-exercises/?topic=" + topic.searchable_name },
        { "text": project_exercise.name, "link": None }
    ]


    # Sending in completed project exercise in case user already completed it
    completed_project_exercise = None


    # Receiving the submitted github link for the exercise
    if request.method == "POST":
        github_link = request.POST.get("github-link")

        # Creating completed project exercise with no score
        completed_project_exercise = models.CompletedProjectExercise(project_exercise=project_exercise, github_link=github_link)
        completed_project_exercise.save()

        # Adding completed project to user
        current_user_profile = request.user.profile
        current_user_profile.completed_project_exercises.add(completed_project_exercise)
        current_user_profile.save()

        # Sending user a message
        message = "Project submitted successfully!"


    # Checking if user already completed project
    user_already_completed_project = False
    for completed_project_exercise in list(request.user.profile.completed_project_exercises.all()):
        if completed_project_exercise.project_exercise == project_exercise:
            user_already_completed_project = True


    return render(request, "home/exercises/project-exercises/project-exercise.html", context={
        "exercise": project_exercise,
        "resources": list(project_exercise.resources.all()),
        "user_already_completed_project": user_already_completed_project,
        "completed_project_exercise": completed_project_exercise,
        "breadcrumbs": breadcrumbs,
        "message": message,
    })
