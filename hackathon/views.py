from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from main.models import Hackathon, Project, Profile


# @login_required(login_url="http://www.w3hacks.com/login")
def index(request, hackathon_id):
    print(request.user.is_authenticated)
    hackathon = Hackathon.objects.get(id=hackathon_id)
    return render(request, "hackathon/index.html", context={
        "hackathon": hackathon
    })


# @login_required(login_url="http://www.w3hacks.com/login")
def competitors(request, hackathon_id):
    hackathon = Hackathon.objects.get(id=hackathon_id)

    # Grabbing competitors
    competitors = list(hackathon.competitors.all())

    return render(request, "hackathon/competitors.html", context={
        "hackathon": hackathon,
        "competitors": competitors
    })


# @login_required(login_url="http://www.w3hacks.com/login")
def schedule(request, hackathon_id):
    hackathon = Hackathon.objects.get(id=hackathon_id)

    # Grabbing ScheduleEvents
    schedule_events = list(hackathon.schedule.all())

    return render(request, "hackathon/schedule.html", context={
        "schedule_events": schedule_events,
        "hackathon": hackathon
    })


# @login_required(login_url="http://www.w3hacks.com/login")
def submissions(request, hackathon_id):
    hackathon = Hackathon.objects.get(id=hackathon_id)

    # Grabbing submissions
    submissions = list(hackathon.submissions.all())

    return render(request, "hackathon/submissions.html", context={
        "hackathon": hackathon,
        "submissions": submissions
    })


# @login_required(login_url="http://www.w3hacks.com/login")
def submit(request, hackathon_id):
    hackathon = Hackathon.objects.get(id=hackathon_id)

    if request.method == "POST":
        # Grabbing form POST data
        title = request.POST.get("title")
        description = request.POST.get("description")
        technologies_used = request.POST.get("technologies-used").split(",") # Splitting into array by commas
        github_link = request.POST.get("github-link")
        project_link = request.POST.get("project-link")
        video_link = request.POST.get("video-link")

        # Creating Project model
        project = Project(
            title=title,
            description=description,
            technologies_used=technologies_used,
            github_link=github_link,
            project_link=project_link,
            video_link=video_link
        )

        # Checking to see if project image was provided
        if "project-image" in request.FILES:
            project.project_image = request.FILES["project-image"]

        # Checking to see if extra files were provided
        if "extra-files" in request.FILES:
            project.project_image = request.FILES["extra-files"]

        # Setting creator to currently signed in user
        print(request.user)
        project.creator = Profile.objects.get(user=request.user)

        project.save()

        return HttpResponseRedirect(f"/{hackathon.id}/submissions/")

    return render(request, "hackathon/submit.html", context={
        "hackathon": hackathon
    })
