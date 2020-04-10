from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from main.models import Hackathon, Project, Profile
from datetime import datetime
from pytz import timezone


def index_redirect(request):
    all_hackathons = Hackathon.objects.all()

    # First, look for a current hackathon
    current_hackathon = None
    for hackathon in all_hackathons:
        if hackathon.start_datetime.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S") < datetime.now().astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S") < hackathon.end_datetime.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S"):
            current_hackathon = hackathon
            break

    if not current_hackathon:
        # Look for upcoming hackathon
        for hackathon in all_hackathons:
            # If current_hackathon is already initalized
            if current_hackathon:
                # Check if the hackathon starts after right now, but before the current hackathon making it earlier
                if datetime.now().astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S") < hackathon.start_datetime.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S") < current_hackathon.start_datetime.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S"):
                    current_hackathon = hackathon
            else:
                # Check if the hackathon starts after right now
                if datetime.now().astimezone(timezone('US/Pacific')).astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S") < hackathon.start_datetime.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S"):
                    current_hackathon = hackathon

    return HttpResponseRedirect("/" + current_hackathon.id)

# @login_required(login_url="http://www.w3hacks.com/login")
def index(request, hackathon_id):
    hackathon = Hackathon.objects.get(id=hackathon_id)

    # Grabbing themes
    themes = list(hackathon.themes.all())

    # Grabbing awards
    awards = list(hackathon.awards.all())

    # Grabbing resource links
    resource_links = list(hackathon.resources.all())

    # Grabbing user's profile
    profile = Profile.objects.get(user=request.user)

    # Checking if user is a competitor
    user_is_competitor = profile in list(hackathon.competitors.all())

    # Getting hackathon starting datetime and converting from UTC to PST
    start_datetime = hackathon.start_datetime.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S")

    # Variable to show if the hackathon started already
    hackathon_already_started = datetime.now().astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S") > start_datetime

    return render(request, "hackathon/index.html", context={
        "hackathon": hackathon,
        "themes": themes,
        "awards": awards,
        "resource_links": resource_links,
        "profile": profile,
        "user_is_competitor": user_is_competitor,
        "hackathon_already_started": hackathon_already_started,
        "start_datetime": start_datetime
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

    # Grabbing current user's submission from submissions if it exists
    user_submission = None
    for i in range(len(submissions)):
        submission = submissions[i]
        if submission.creator == Profile.objects.get(user=request.user):
            user_submission = submission # Setting user_submission to the user's submission
            submissions.pop(i) # Removing user's submission from the other submissions
            break


    if request.method == "POST":
        # Grab project
        project_id = request.GET.get("project_id")
        project = Profile.objects.get(id=project_id)

        # If the creator of the project is equal to the one deleting it you can delete it
        if project.creator.user == request.user:
            # Delete the project
            hackathon.submissions.remove(project)

        project.delete()


    return render(request, "hackathon/submissions.html", context={
        "hackathon": hackathon,
        "submissions": submissions,
        "user_submission": user_submission
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

        # Adding project to submissions
        hackathon.submissions.add(project)
        hackathon.save()

        return HttpResponseRedirect(f"/{hackathon.id}/submissions/")


    # Define user_already_submitted -> only allow submission from user if the user hasn't submitted yet
    user_already_submitted = False
    for submission in list(hackathon.submissions.all()):
        if Profile.objects.get(user=request.user) == submission.creator:  # This submission was submitted by current user
            user_already_submitted = True

    # Define too_early and too_late -> defines if the user is too early or too late to submit
    too_early = hackathon.submissions_open_datetime.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S") > datetime.now().astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S")
    too_late = hackathon.submissions_close_datetime.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S") < datetime.now().astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S")

    # Getting opening and closing submissions datetimes
    submissions_open_datetime = hackathon.submissions_open_datetime.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S")
    submissions_close_datetime = hackathon.submissions_close_datetime.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S")

    # Define profile and competitors
    profile = Profile.objects.get(user=request.user)
    competitors = list(hackathon.competitors.all())

    return render(request, "hackathon/submit.html", context={
        "hackathon": hackathon,
        "too_early": too_early,
        "too_late": too_late,
        "user_already_submitted": user_already_submitted,
        "profile": profile,
        "competitors": competitors,
        "submissions_open_datetime": submissions_open_datetime,
        "submissions_close_datetime": submissions_close_datetime
    })


def awards(request, hackathon_id):
    hackathon = Hackathon.objects.get(id=hackathon_id)

    show_winners = datetime.now().astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S") > hackathon.winners_announced.astimezone(timezone('US/Pacific')).strftime("%m/%d/%Y %H:%M:%S")

    return render(request, "hackathon/awards.html", context={
        "hackathon": hackathon,
        "show_winners": show_winners
    })
