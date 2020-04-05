from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models

# ALL IDs MUST BE 8 CHARACTERS LONG

# Making the default Django user's username and email unique
User._meta.get_field('username')._unique = True
User._meta.get_field('email')._unique = True

# An extension off of the default User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", unique=True) # Extending from default User class
    status = models.CharField(max_length=20, null=True, blank=True) # OPTIONAL: A quick status that the user may update
    biography = models.TextField(max_length=200, null=True, blank=True) # OPTIONAL: A description of the user
    birthday = models.DateField(null=True, blank=True) # OPTIONAL: The birthday of the user
    education = models.CharField(max_length=100, null=True, blank=True) # OPTIONAL: The current/past education of the user
    location = models.CharField(max_length=50, null=True, blank=True) # OPTIONAL: The area around where the user lives
    profile_picture = models.ImageField(null=True, blank=True) # OPTIONAL: A profile picture for the user
    skills = ArrayField(models.CharField(max_length=50), null=True, blank=True) # OPTIONAL: An array of the user's skills
    social_links = models.ManyToManyField("SocialLink", blank=True) # OPTIONAL: A list of social links for the user
    past_hackathons = models.ManyToManyField("Hackathon", blank=True) # OPTIONAL: A lit of past w3Hacks hackathons that the user has competed in
    projects = models.ManyToManyField("Project", blank=True) # List of projects created by user
    # followers = models.ManyToManyField("Profile", blank=True) # OPTIONAL: A list of profiles that follow self user
    # following = models.ManyToManyField("Profile", blank=True) # OPTIONAL: A list of profiles that this user follows
    joined_date = models.DateField() # The date when the user joined w3Hacks
    credits = models.IntegerField() # The number of credits the user has
    overall_ranking_points = models.IntegerField() # The overall ranking points the user has
    project_ranking_points = models.IntegerField() # The project ranking points the user has
    quiz_ranking_points = models.IntegerField() # The quiz ranking points the user has
    exercise_ranking_points = models.IntegerField() # The exercise ranking points the user has

    def __str__(self):
        return self.user.username


# Project model for each project
class Project(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True) # Unique ID for project
    title = models.CharField(max_length=50) # Name of the project
    description = models.TextField(max_length=500) # Description of the project
    project_image = models.ImageField(null=True, blank=True) # OPTIONAL: Image of the project
    technologies_used = ArrayField(models.CharField(max_length=30), null=True, blank=True) # OPTIONAL: Array of technologies used for the project
    github_link = models.CharField(max_length=200, null=True, blank=True) # OPTIONAL: Link to the project on GitHub
    project_link = models.CharField(max_length=200, null=True, blank=True) # OPTIONAL: Link to the project if hosted on the app store or Internet
    video_link = models.CharField(max_length=200, null=True, blank=True) # OPTIONAL: Link to a video of project demo
    extra_files = ArrayField(models.FileField(), null=True, blank=True) # OPTIONAL: Array of extra files to submit along with project
    creator = models.ForeignKey("Profile", on_delete=models.PROTECT) # Creator of project
    likes = models.IntegerField(null=True, blank=True) # OPTIONAL: Number of likes on project

    def __str__(self):
        return self.title


# Model for each hackathon, current or not
class Hackathon(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True) # ID for display
    title = models.CharField(max_length=50) # Name of the hackathon
    description = models.TextField(max_length=300) # Description of the hackathon
    themes = models.ManyToManyField("Theme", blank=True) # List of themes for hackathon
    awards = models.ManyToManyField("Award", blank=True) # List of awards for hackathon
    start_datetime = models.DateTimeField() # Starting datetime for the hackathon
    end_datetime = models.DateTimeField() # Ending datetime for the hackathon
    schedule = models.ManyToManyField("ScheduleEvent", blank=True) # List of ScheduleEvents for hackathon
    resources = models.ManyToManyField("ResourceLink", blank=True) # List of resource links for hackathon
    competitors = models.ManyToManyField("Profile", blank=True) # List of competitor profiles; can be empty in beginning
    submissions = models.ManyToManyField("Project", blank=True) # List of project submissions; can be empty in beginning

    def __str__(self):
        return self.title


# For 'Themes' section of Hackathon
class Theme(models.Model):
    title = models.CharField(max_length=50) # Name of the theme
    description = models.TextField(max_length=300) # Description of the theme

    def __str__(self):
        return self.title


# For 'Resources' section of Hackathon
class ResourceLink(models.Model):
    title = models.CharField(max_length=50) # String to be shown on display
    url_extension = models.CharField(max_length=50, unique=True) # String for url extension
    link = models.CharField(max_length=200) # Actual link URL

    def __str__(self):
        return self.title


# For user profile social links
class SocialLink(models.Model):
    social_network = models.CharField(max_length=50) # Name of social network
    link = models.CharField(max_length=200) # Actual social link URL

    def __str__(self):
        return self.social_network


# For each award for Hackathon
class Award(models.Model):
    title = models.CharField(max_length=50) # Name of the award
    description = models.TextField(max_length=300) # Description of the award
    prize = models.CharField(max_length=100) # Prize for the winner of the award
    winner = models.ForeignKey("Profile", on_delete=models.PROTECT, null=True, blank=True) # Winner of the award

    def __str__(self):
        return self.name


# For each event on Hackathon schedule
class ScheduleEvent(models.Model):
    title = models.CharField(max_length=50) # Name of the event
    description = models.TextField(max_length=300) # Description of the event
    event_link = models.CharField(max_length=200, null=True, blank=True) # OPTIONAL: Link for the event

    def __str__(self):
        return self.title
