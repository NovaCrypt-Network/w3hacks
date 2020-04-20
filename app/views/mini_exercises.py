from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from main import models


@login_required(login_url="http://www.w3hacks.com/login")
def mini_exercises(request):
    return render(request, "app/exercises/mini-exercises/mini-exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def fix_the_code_exercises(request):
    topics = models.Topic.objects.all()
    fix_the_code_exercises = models.FixTheCodeExercise.objects.all()
    specific_topic = None

    if request.GET.get("topic"):
        topic = request.GET.get("topic")

        # Iterating through project exercises to find ones that are in the topic
        iterable_fix_the_code_exercises = fix_the_code_exercises
        fix_the_code_exercises = []
        for fix_the_code_exercise in iterable_fix_the_code_exercises:
            if fix_the_code_exercise.topic.searchable_name == topic:
                fix_the_code_exercises.append(fix_the_code_exercise)

        # Topic object to pass into template
        specific_topic = models.Topic.objects.get(searchable_name=topic)


    return render(request, "app/exercises/mini-exercises/fix-the-code-exercises.html", context={
        "topics": topics,
        "exercises": fix_the_code_exercises,
        "topic": specific_topic
    })

    return render(request, "app/exercises/mini-exercises/fix-the-code-exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def fix_the_code_exercise(request):
    fix_the_code_exercise_id = request.GET.get("id")
    if fix_the_code_exercise_id:
        if models.FixTheCodeExercise.objects.filter(id=fix_the_code_exercise_id).exists():
            fix_the_code_exercise = models.FixTheCodeExercise.objects.get(id=fix_the_code_exercise_id)
        else:
            return HttpResponse("Invalid exercise ID.")
    else:
        return HttpResponse("You must provide an exercise ID.")


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


    return render(request, "app/exercises/mini-exercises/fix-the-code-exercise.html", context={
        "exercise": fix_the_code_exercise,
        "resources": list(fix_the_code_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_fix_the_code_exercise": completed_fix_the_code_exercise,
        "message": message
    })


@login_required(login_url="http://www.w3hacks.com/login")
def brainteaser_exercises(request):
    topics = models.Topic.objects.all()
    brainteaser_exercises = models.BrainTeaserExercise.objects.all()
    specific_topic = None

    if request.GET.get("topic"):
        topic = request.GET.get("topic")

        # Iterating through project exercises to find ones that are in the topic
        iterable_brainteaser_exercises = brainteaser_exercises
        brainteaser_exercises = []
        for brainteaser_exercise in iterable_brainteaser_exercises:
            if brainteaser_exercise.topic.searchable_name == topic:
                brainteaser_exercises.append(brainteaser_exercise)

        # Topic object to pass into template
        specific_topic = models.Topic.objects.get(searchable_name=topic)

    return render(request, "app/exercises/mini-exercises/brainteaser-exercises.html", context={
        "topics": topics,
        "exercises": brainteaser_exercises,
        "topic": specific_topic
    })

    return render(request, "app/exercises/mini-exercises/brainteaser-exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def brainteaser_exercise(request):
    brainteaser_exercise_id = request.GET.get("id")
    if brainteaser_exercise_id:
        if models.BrainTeaserExercise.objects.filter(id=brainteaser_exercise_id).exists():
            brainteaser_exercise = models.BrainTeaserExercise.objects.get(id=brainteaser_exercise_id)
        else:
            return HttpResponse("Invalid exercise ID.")
    else:
        return HttpResponse("You must provide an exercise ID.")

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


    return render(request, "app/exercises/mini-exercises/brainteaser-exercise.html", context={
        "exercise": brainteaser_exercise,
        "resources": list(brainteaser_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_brainteaser_exercise": completed_brainteaser_exercise,
        "message": message
    })


@login_required(login_url="http://www.w3hacks.com/login")
def visualization_exercises(request):
    topics = models.Topic.objects.all()
    visualization_exercises = models.VisualizationExercise.objects.all()
    specific_topic = None

    if request.GET.get("topic"):
        topic = request.GET.get("topic")

        # Iterating through project exercises to find ones that are in the topic
        iterable_visualization_exercises = visualization_exercises
        visualization_exercises = []
        for visualization_exercise in iterable_visualization_exercises:
            if visualization_exercise.topic.searchable_name == topic:
                visualization_exercises.append(visualization_exercise)

        # Topic object to pass into template
        specific_topic = models.Topic.objects.get(searchable_name=topic)

    return render(request, "app/exercises/mini-exercises/visualization-exercises.html", context={
        "topics": topics,
        "exercises": visualization_exercises,
        "topic": specific_topic
    })

    return render(request, "app/exercises/mini-exercises/visualization-exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def visualization_exercise(request):
    visualization_exercise_id = request.GET.get("id")
    if visualization_exercise_id:
        if models.VisualizationExercise.objects.filter(id=visualization_exercise_id).exists():
            visualization_exercise = models.VisualizationExercise.objects.get(id=visualization_exercise_id)
        else:
            return HttpResponse("Invalid exercise ID.")
    else:
        return HttpResponse("You must provide an exercise ID.")

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


    return render(request, "app/exercises/mini-exercises/visualization-exercise.html", context={
        "exercise": visualization_exercise,
        "resources": list(visualization_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_visualization_exercise": completed_visualization_exercise,
        "message": message
    })


@login_required(login_url="http://www.w3hacks.com/login")
def refactor_exercises(request):
    topics = models.Topic.objects.all()
    refactor_exercises = models.RefactorExercise.objects.all()
    specific_topic = None

    if request.GET.get("topic"):
        topic = request.GET.get("topic")

        # Iterating through project exercises to find ones that are in the topic
        iterable_refactor_exercises = refactor_exercises
        refactor_exercises = []
        for refactor_exercise in iterable_refactor_exercises:
            if refactor_exercise.topic.searchable_name == topic:
                refactor_exercises.append(refactor_exercise)

        # Topic object to pass into template
        specific_topic = models.Topic.objects.get(searchable_name=topic)

    return render(request, "app/exercises/mini-exercises/refactor-exercises.html", context={
        "topics": topics,
        "exercises": refactor_exercises,
        "topic": specific_topic
    })

    return render(request, "app/exercises/mini-exercises/refactor-exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def refactor_exercise(request):
    refactor_exercise_id = request.GET.get("id")
    if refactor_exercise_id:
        if models.RefactorExercise.objects.filter(id=refactor_exercise_id).exists():
            refactor_exercise = models.RefactorExercise.objects.get(id=refactor_exercise_id)
        else:
            return HttpResponse("Invalid exercise ID.")
    else:
        return HttpResponse("You must provide an exercise ID.")

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


    return render(request, "app/exercises/mini-exercises/refactor-exercise.html", context={
        "exercise": refactor_exercise,
        "resources": list(refactor_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_refactor_exercise": completed_refactor_exercise,
        "message": message
    })


@login_required(login_url="http://www.w3hacks.com/login")
def teaching_exercises(request):
    topics = models.Topic.objects.all()
    teaching_exercises = models.TeachingExercise.objects.all()
    specific_topic = None

    if request.GET.get("topic"):
        topic = request.GET.get("topic")

        # Iterating through project exercises to find ones that are in the topic
        iterable_teaching_exercises = teaching_exercises
        teaching_exercises = []
        for teaching_exercise in iterable_teaching_exercises:
            if teaching_exercise.topic.searchable_name == topic:
                teaching_exercises.append(teaching_exercise)

        # Topic object to pass into template
        specific_topic = models.Topic.objects.get(searchable_name=topic)

    return render(request, "app/exercises/mini-exercises/teaching-exercises.html", context={
        "topics": topics,
        "exercises": teaching_exercises,
        "topic": specific_topic
    })

    return render(request, "app/exercises/mini-exercises/teaching-exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def teaching_exercise(request):
    teaching_exercise_id = request.GET.get("id")
    if teaching_exercise_id:
        if models.TeachingExercise.objects.filter(id=teaching_exercise_id).exists():
            teaching_exercise = models.TeachingExercise.objects.get(id=teaching_exercise_id)
        else:
            return HttpResponse("Invalid exercise ID.")
    else:
        return HttpResponse("You must provide an exercise ID.")

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


    return render(request, "app/exercises/mini-exercises/teaching-exercise.html", context={
        "exercise": teaching_exercise,
        "resources": list(teaching_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_teaching_exercise": completed_teaching_exercise,
        "message": message
    })


@login_required(login_url="http://www.w3hacks.com/login")
def github_exercises(request):
    topics = models.Topic.objects.all()
    github_exercises = models.GitHubExercise.objects.all()
    specific_topic = None

    if request.GET.get("topic"):
        topic = request.GET.get("topic")

        # Iterating through project exercises to find ones that are in the topic
        iterable_github_exercises = github_exercises
        github_exercises = []
        for github_exercise in iterable_github_exercises:
            if github_exercise.topic.searchable_name == topic:
                github_exercises.append(github_exercise)

        # Topic object to pass into template
        specific_topic = models.Topic.objects.get(searchable_name=topic)

    return render(request, "app/exercises/mini-exercises/github-exercises.html", context={
        "topics": topics,
        "exercises": github_exercises,
        "topic": specific_topic
    })

    return render(request, "app/exercises/mini-exercises/github-exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def github_exercise(request):
    github_exercise_id = request.GET.get("id")
    if github_exercise_id:
        if models.GitHubExercise.objects.filter(id=github_exercise_id).exists():
            github_exercise = models.GitHubExercise.objects.get(id=github_exercise_id)
        else:
            return HttpResponse("Invalid exercise ID.")
    else:
        return HttpResponse("You must provide an exercise ID.")

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


    return render(request, "app/exercises/mini-exercises/github-exercise.html", context={
        "exercise": github_exercise,
        "resources": list(github_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_github_exercise": completed_github_exercise,
        "message": message
    })


@login_required(login_url="http://www.w3hacks.com/login")
def research_exercises(request):
    topics = models.Topic.objects.all()
    research_exercises = models.ResearchExercise.objects.all()
    specific_topic = None

    if request.GET.get("topic"):
        topic = request.GET.get("topic")

        # Iterating through project exercises to find ones that are in the topic
        iterable_research_exercises = research_exercises
        research_exercises = []
        for research_exercise in iterable_research_exercises:
            if research_exercise.topic.searchable_name == topic:
                research_exercises.append(research_exercise)

        # Topic object to pass into template
        specific_topic = models.Topic.objects.get(searchable_name=topic)

    return render(request, "app/exercises/mini-exercises/research-exercises.html", context={
        "topics": topics,
        "exercises": research_exercises,
        "topic": specific_topic
    })

    return render(request, "app/exercises/mini-exercises/research-exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def research_exercise(request):
    research_exercise_id = request.GET.get("id")
    if research_exercise_id:
        if models.ResearchExercise.objects.filter(id=research_exercise_id).exists():
            research_exercise = models.ResearchExercise.objects.get(id=research_exercise_id)
        else:
            return HttpResponse("Invalid exercise ID.")
    else:
        return HttpResponse("You must provide an exercise ID.")

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


    return render(request, "app/exercises/mini-exercises/research-exercise.html", context={
        "exercise": research_exercise,
        "resources": list(research_exercise.resources.all()),
        "user_already_completed_mini_exercise": user_already_completed_mini_exercise,
        "completed_research_exercise": completed_research_exercise,
        "message": message
    })
