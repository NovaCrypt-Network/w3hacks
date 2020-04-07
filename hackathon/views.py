from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from main.models import Hackathon, Project, Profile
from datetime import datetime


def index_redirect(request):
    all_hackathons = Hackathon.objects.all()

    # First, look for a current hackathon
    current_hackathon = None
    for hackathon in all_hackathons:
        if hackathon.start_datetime.strftime("%d/%m/%Y %H:%M:%S") < datetime.now().strftime("%d/%m/%Y %H:%M:%S") < hackathon.end_datetime.strftime("%d/%m/%Y %H:%M:%S"):
            current_hackathon = hackathon
            break

    if not current_hackathon:
        # Look for upcoming hackathon
        for hackathon in all_hackathons:
            # If current_hackathon is already initalized
            if current_hackathon:
                # Check if the hackathon starts after right now, but before the current hackathon making it earlier
                if datetime.now().strftime("%d/%m/%Y %H:%M:%S") < hackathon.start_datetime.strftime("%d/%m/%Y %H:%M:%S") < current_hackathon.start_datetime.strftime("%d/%m/%Y %H:%M:%S"):
                    current_hackathon = hackathon
            else:
                # Check if the hackathon starts after right now
                if datetime.now().strftime("%d/%m/%Y %H:%M:%S") < hackathon.start_datetime.strftime("%d/%m/%Y %H:%M:%S"):
                    current_hackathon = hackathon

    return HttpResponseRedirect("/" + current_hackathon.id)

# @login_required(login_url="http://www.w3hacks.com/login")
def index(request, hackathon_id):
    hackathon = Hackathon.objects.get(id=hackathon_id)

    # Checking to see if we should show themes now or now
    show_themes = datetime.now().strftime("%d/%m/%Y %H:%M:%S") > hackathon.start_datetime.strftime("%d/%m/%Y %H:%M:%S")

    # Grabbing themes if hackathon has started or passed
    themes = None
    if show_themes:
        themes = list(hackathon.themes.all())

    # Grabbing awards
    awards = list(hackathon.awards.all())

    # Grabbing resource links
    resource_links = list(hackathon.resources.all())

    return render(request, "hackathon/index.html", context={
        "hackathon": hackathon,
        "themes": themes,
        "awards": awards,
        "resource_links": resource_links
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
        project.creator = Profile.objects.get(user=request.user)

        project.save()

        return HttpResponseRedirect(f"/{hackathon.id}/submissions/")


    # Define user_already_submitted -> only allow submission from user if the user hasn't submitted yet
    user_already_submitted = False
    for submission in list(hackathon.submissions.all()):
        if Profile.objects.get(user=request.user) == submission.creator:  # This submission was submitted by current user
            user_already_submitted = True

    # Define allow_submit -> only allow submissions if right now is between hackathon start and end datetime
    allow_submit = hackathon.end_datetime.strftime("%d/%m/%Y %H:%M:%S") > datetime.now().strftime("%d/%m/%Y %H:%M:%S") > hackathon.start_datetime.strftime("%d/%m/%Y %H:%M:%S")

    return render(request, "hackathon/submit.html", context={
        "hackathon": hackathon,
        "allow_submit": allow_submit,
        "user_already_submitted": user_already_submitted
    })
