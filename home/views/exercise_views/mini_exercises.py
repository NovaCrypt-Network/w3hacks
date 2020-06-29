from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from main import models


@login_required(login_url="/login/")
def mini_exercises(request):
    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": None }
    ]

    return render(request, "home/exercises/mini-exercises/mini-exercises.html", context={
        "breadcrumbs": breadcrumbs
    })


@login_required(login_url="/login/")
def fix_the_code_exercises(request):
    fix_the_code_exercises = models.FixTheCodeExercise.objects.all()
    specific_topic = None

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Fix The Code", "link": "/exercises/mini-exercises/fix-the-code-exercises/" }
    ]


    return render(request, "home/exercises/mini-exercises/fix-the-code-exercises.html", context={
        "breadcrumbs": breadcrumbs,
        "exercises": fix_the_code_exercises,
        "topic": specific_topic
    })

    return render(request, "home/exercises/mini-exercises/fix-the-code-exercises.html")


@login_required(login_url="/login/")
def fix_the_code_exercise(request):
    fix_the_code_exercise_id = request.GET.get("id")
    if fix_the_code_exercise_id:
        if models.FixTheCodeExercise.objects.filter(id=fix_the_code_exercise_id).exists():
            fix_the_code_exercise = models.FixTheCodeExercise.objects.get(id=fix_the_code_exercise_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Fix The Code", "link": "/exercises/mini-exercises/fix-the-code-exercises/" },
        { "text": fix_the_code_exercise.name, "link": None }
    ]

    # Sending in completed project exercise in case user already completed it
    completed_fix_the_code_exercise = None
    message = None

    # Receiving the submitted github link for the exercise
    if request.method == "POST":
        repl_link = request.POST.get("repl-link")

        # Creating completed project exercise with no score
        completed_fix_the_code_exercise = models.CompletedFixTheCodeExercise(fix_the_code_exercise=fix_the_code_exercise, repl_link=repl_link)
        completed_fix_the_code_exercise.save()

        # Adding completed project to user
        current_user_profile = request.user.profile
        current_user_profile.completed_fix_the_code_exercises.add(completed_fix_the_code_exercise)
        current_user_profile.save()

        # Sending user a message
        message = "Fix The Code Mini Exercise submitted successfully!"


    # Checking if user already completed project
    user_already_completed_mini_exercise = False
    for completed_fix_the_code_exercise in list(request.user.profile.completed_fix_the_code_exercises.all()):
        if completed_fix_the_code_exercise.fix_the_code_exercise == fix_the_code_exercise:
            user_already_completed_mini_exercise = True


    return render(request, "home/exercises/mini-exercises/fix-the-code-exercise.html", context={
        "exercise": fix_the_code_exercise,
        "resources": list(fix_the_code_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_fix_the_code_exercise": completed_fix_the_code_exercise,
        "breadcrumbs": breadcrumbs,
        "message": message
    })


@login_required(login_url="/login/")
def brainteaser_exercises(request):
    brainteaser_exercises = models.BrainTeaserExercise.objects.all()
    specific_topic = None

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Brain Teaser", "link": "/exercises/mini-exercises/brainteaser-exercises/" }
    ]

    return render(request, "home/exercises/mini-exercises/brainteaser-exercises.html", context={
        "exercises": brainteaser_exercises,
        "breadcrumbs": breadcrumbs,
        "topic": specific_topic
    })

    return render(request, "home/exercises/mini-exercises/brainteaser-exercises.html")


@login_required(login_url="/login/")
def brainteaser_exercise(request):
    brainteaser_exercise_id = request.GET.get("id")
    if brainteaser_exercise_id:
        if models.BrainTeaserExercise.objects.filter(id=brainteaser_exercise_id).exists():
            brainteaser_exercise = models.BrainTeaserExercise.objects.get(id=brainteaser_exercise_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Brain Teaser", "link": "/exercises/mini-exercises/brainteaser-exercises/" },
        { "text": brainteaser_exercise.name, "link": None }
    ]

    # Sending in completed project exercise in case user already completed it
    completed_brainteaser_exercise = None
    message = None

    # Receiving the submitted github link for the exercise
    if request.method == "POST":
        repl_link = request.POST.get("repl-link")

        # Creating completed project exercise with no score
        completed_brainteaser_exercise = models.CompletedBrainTeaserExercise(brainteaser_exercise=brainteaser_exercise, repl_link=repl_link)
        completed_brainteaser_exercise.save()

        # Adding completed project to user
        current_user_profile = request.user.profile
        current_user_profile.completed_brainteaser_exercises.add(completed_brainteaser_exercise)
        current_user_profile.save()

        # Sending user a message
        message = "BrainTeaser Mini Exercise submitted successfully!"


    # Checking if user already completed project
    user_already_completed_mini_exercise = False
    for completed_brainteaser_exercise in list(request.user.profile.completed_brainteaser_exercises.all()):
        if completed_brainteaser_exercise.brainteaser_exercise == brainteaser_exercise:
            user_already_completed_mini_exercise = True


    return render(request, "home/exercises/mini-exercises/brainteaser-exercise.html", context={
        "exercise": brainteaser_exercise,
        "resources": list(brainteaser_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_brainteaser_exercise": completed_brainteaser_exercise,
        "breadcrumbs": breadcrumbs,
        "message": message
    })


@login_required(login_url="/login/")
def visualization_exercises(request):
    visualization_exercises = models.VisualizationExercise.objects.all()
    specific_topic = None

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Visualize It!", "link": "/exercises/mini-exercises/visualization-exercises/" }
    ]

    return render(request, "home/exercises/mini-exercises/visualization-exercises.html", context={
        "exercises": visualization_exercises,
        "breadcrumbs": breadcrumbs,
        "topic": specific_topic
    })

    return render(request, "home/exercises/mini-exercises/visualization-exercises.html")


@login_required(login_url="/login/")
def visualization_exercise(request):
    visualization_exercise_id = request.GET.get("id")
    if visualization_exercise_id:
        if models.VisualizationExercise.objects.filter(id=visualization_exercise_id).exists():
            visualization_exercise = models.VisualizationExercise.objects.get(id=visualization_exercise_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Visualize It!", "link": "/exercises/mini-exercises/visualization-exercises/" },
        { "text": visualization_exercise.name, "link": None }
    ]


    # Sending in completed project exercise in case user already completed it
    completed_visualization_exercise = None
    message = None

    # Receiving the submitted github link for the exercise
    if request.method == "POST":
        # Creating completed project exercise with no score
        completed_visualization_exercise = models.CompletedVisualizationExercise(visualization_exercise=visualization_exercise)
        completed_visualization_exercise.visualization_file = request.FILES["visualization-file"] # Setting visualization file to visualization exercise
        completed_visualization_exercise.save()

        # Adding completed project to user
        current_user_profile = request.user.profile
        current_user_profile.completed_visualization_exercises.add(completed_visualization_exercise)
        current_user_profile.save()

        # Sending user a message
        message = "Visualization Mini Exercise submitted successfully!"


    # Checking if user already completed project
    user_already_completed_mini_exercise = False
    for completed_visualization_exercise in list(request.user.profile.completed_visualization_exercises.all()):
        if completed_visualization_exercise.visualization_exercise == visualization_exercise:
            user_already_completed_mini_exercise = True


    return render(request, "home/exercises/mini-exercises/visualization-exercise.html", context={
        "exercise": visualization_exercise,
        "resources": list(visualization_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_visualization_exercise": completed_visualization_exercise,
        "breadcrumbs": breadcrumbs,
        "message": message
    })


@login_required(login_url="/login/")
def refactor_exercises(request):
    refactor_exercises = models.RefactorExercise.objects.all()
    specific_topic = None

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Refactor It!", "link": "/exercises/mini-exercises/refactor-exercises/" }
    ]

    return render(request, "home/exercises/mini-exercises/refactor-exercises.html", context={
        "exercises": refactor_exercises,
        "topic": specific_topic,
        "breadcrumbs": breadcrumbs
    })

    return render(request, "home/exercises/mini-exercises/refactor-exercises.html")


@login_required(login_url="/login/")
def refactor_exercise(request):
    refactor_exercise_id = request.GET.get("id")
    if refactor_exercise_id:
        if models.RefactorExercise.objects.filter(id=refactor_exercise_id).exists():
            refactor_exercise = models.RefactorExercise.objects.get(id=refactor_exercise_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Refactor It!", "link": "/exercises/mini-exercises/refactor-exercises/" },
        { "text": refactor_exercise.name, "link": None }
    ]


    # Sending in completed project exercise in case user already completed it
    completed_refactor_exercise = None
    message = None

    # Receiving the submitted github link for the exercise
    if request.method == "POST":
        repl_link = request.POST.get("repl-link")

        # Creating completed project exercise with no score
        completed_refactor_exercise = models.CompletedRefactorExercise(refactor_exercise=refactor_exercise, repl_link=repl_link)
        completed_refactor_exercise.save()

        # Adding completed project to user
        current_user_profile = request.user.profile
        current_user_profile.completed_refactor_exercises.add(completed_refactor_exercise)
        current_user_profile.save()

        # Sending user a message
        message = "Refactor Mini Exercise submitted successfully!"


    # Checking if user already completed project
    user_already_completed_mini_exercise = False
    for completed_refactor_exercise in list(request.user.profile.completed_refactor_exercises.all()):
        if completed_refactor_exercise.refactor_exercise == refactor_exercise:
            user_already_completed_mini_exercise = True


    return render(request, "home/exercises/mini-exercises/refactor-exercise.html", context={
        "exercise": refactor_exercise,
        "resources": list(refactor_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_refactor_exercise": completed_refactor_exercise,
        "breadcrumbs": breadcrumbs,
        "message": message
    })


@login_required(login_url="/login/")
def teaching_exercises(request):
    teaching_exercises = models.TeachingExercise.objects.all()
    specific_topic = None

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Teach It!", "link": "/exercises/mini-exercises/teaching-exercises/" }
    ]

    return render(request, "home/exercises/mini-exercises/teaching-exercises.html", context={
        "exercises": teaching_exercises,
        "topic": specific_topic,
        "breadcrumbs": breadcrumbs,
    })


@login_required(login_url="/login/")
def teaching_exercise(request):
    teaching_exercise_id = request.GET.get("id")
    if teaching_exercise_id:
        if models.TeachingExercise.objects.filter(id=teaching_exercise_id).exists():
            teaching_exercise = models.TeachingExercise.objects.get(id=teaching_exercise_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Teach It!", "link": "/exercises/mini-exercises/teaching-exercises/" },
        { "text": teaching_exercise.name, "link": None }
    ]


    # Sending in completed project exercise in case user already completed it
    completed_teaching_exercise = None
    message = None

    # Receiving the submitted github link for the exercise
    if request.method == "POST":
        teaching_exercise_link = request.POST.get("teaching-exercise-link")

        # Creating completed project exercise with no score
        completed_teaching_exercise = models.CompletedTeachingExercise(teaching_exercise=teaching_exercise, teaching_exercise_link=teaching_exercise_link)
        completed_teaching_exercise.save()

        # Adding completed project to user
        current_user_profile = request.user.profile
        current_user_profile.completed_teaching_exercises.add(completed_teaching_exercise)
        current_user_profile.save()

        # Sending user a message
        message = "Teaching Mini Exercise submitted successfully!"


    # Checking if user already completed project
    user_already_completed_mini_exercise = False
    for completed_teaching_exercise in list(request.user.profile.completed_teaching_exercises.all()):
        if completed_teaching_exercise.teaching_exercise == teaching_exercise:
            user_already_completed_mini_exercise = True


    return render(request, "home/exercises/mini-exercises/teaching-exercise.html", context={
        "exercise": teaching_exercise,
        "resources": list(teaching_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_teaching_exercise": completed_teaching_exercise,
        "breadcrumbs": breadcrumbs,
        "message": message
    })


@login_required(login_url="/login/")
def github_exercises(request):
    github_exercises = models.GitHubExercise.objects.all()
    specific_topic = None

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Git/GitHub", "link": "/exercises/mini-exercises/github-exercises/" }
    ]

    return render(request, "home/exercises/mini-exercises/github-exercises.html", context={
        "exercises": github_exercises,
        "breadcrumbs": breadcrumbs,
        "topic": specific_topic
    })

    return render(request, "home/exercises/mini-exercises/github-exercises.html")


@login_required(login_url="/login/")
def github_exercise(request):
    github_exercise_id = request.GET.get("id")
    if github_exercise_id:
        if models.GitHubExercise.objects.filter(id=github_exercise_id).exists():
            github_exercise = models.GitHubExercise.objects.get(id=github_exercise_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Git/GitHub", "link": "/exercises/mini-exercises/github-exercises/" },
        { "text": github_exercise.name, "link": None }
    ]


    # Sending in completed project exercise in case user already completed it
    completed_github_exercise = None
    message = None

    # Receiving the submitted github link for the exercise
    if request.method == "POST":
        github_exercise_link = request.POST.get("github-exercise-link")

        # Creating completed project exercise with no score
        completed_github_exercise = models.CompletedGitHubExercise(github_exercise=github_exercise, github_exercise_link=github_exercise_link)
        completed_github_exercise.save()

        # Adding completed project to user
        current_user_profile = request.user.profile
        current_user_profile.completed_github_exercises.add(completed_github_exercise)
        current_user_profile.save()

        # Sending user a message
        message = "GitHub Mini Exercise submitted successfully!"


    # Checking if user already completed project
    user_already_completed_mini_exercise = False
    for completed_github_exercise in list(request.user.profile.completed_github_exercises.all()):
        if completed_github_exercise.github_exercise == github_exercise:
            user_already_completed_mini_exercise = True


    return render(request, "home/exercises/mini-exercises/github-exercise.html", context={
        "exercise": github_exercise,
        "resources": list(github_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_github_exercise": completed_github_exercise,
        "breadcrumbs": breadcrumbs,
        "message": message
    })


@login_required(login_url="/login/")
def research_exercises(request):
    research_exercises = models.ResearchExercise.objects.all()
    specific_topic = None

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Research It!", "link": "/exercises/mini-exercises/research-exercises/" }
    ]

    return render(request, "home/exercises/mini-exercises/research-exercises.html", context={
        "exercises": research_exercises,
        "breadcrumbs": breadcrumbs,
        "topic": specific_topic
    })

    return render(request, "home/exercises/mini-exercises/research-exercises.html")


@login_required(login_url="/login/")
def research_exercise(request):
    research_exercise_id = request.GET.get("id")
    if research_exercise_id:
        if models.ResearchExercise.objects.filter(id=research_exercise_id).exists():
            research_exercise = models.ResearchExercise.objects.get(id=research_exercise_id)
        else:
            return render(request, "errors/exercise-does-not-exist.html")
    else:
        return render(request, "errors/exercise-does-not-exist.html")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/" },
        { "text": "Mini Exercises", "link": "/exercises/mini-exercises/" },
        { "text": "Research It!", "link": "/exercises/mini-exercises/research-exercises/" },
        { "text": research_exercise.name, "link": None }
    ]


    # Sending in completed project exercise in case user already completed it
    completed_research_exercise = None
    message = None

    # Receiving the submitted github link for the exercise
    if request.method == "POST":
        research_link = request.POST.get("research-link")

        # Creating completed project exercise with no score
        completed_research_exercise = models.CompletedResearchExercise(research_exercise=research_exercise, research_link=research_link)
        completed_research_exercise.save()

        # Adding completed project to user
        current_user_profile = request.user.profile
        current_user_profile.completed_research_exercises.add(completed_research_exercise)
        current_user_profile.save()

        # Sending user a message
        message = "Research Mini Exercise submitted successfully!"


    # Checking if user already completed project
    user_already_completed_mini_exercise = False
    for completed_research_exercise in list(request.user.profile.completed_research_exercises.all()):
        if completed_research_exercise.research_exercise == research_exercise:
            user_already_completed_mini_exercise = True


    return render(request, "home/exercises/mini-exercises/research-exercise.html", context={
        "exercise": research_exercise,
        "resources": list(research_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_research_exercise": completed_research_exercise,
        "breadcrumbs": breadcrumbs,
        "message": message
    })
