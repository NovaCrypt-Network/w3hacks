from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models
from datetime import date, datetime
import random
import string

# ALL IDs MUST BE 8 CHARACTERS LONG
def generate_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])

# Making the default Django user's username and email unique
User._meta.get_field('username')._unique = True
User._meta.get_field('email')._unique = True



####################
## GENERAL MODELS ##
####################

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

    github_profile = models.CharField(max_length=100, null=True, blank=True) # OPTIONAL: Link to user's GitHub profile
    linkedin_profile = models.CharField(max_length=100, null=True, blank=True) # OPTIONAL: Link to user's LinkedIn profile
    twitter_profile = models.CharField(max_length=100, null=True, blank=True) # OPTIONAL: Link to user's Twitter profile
    instagram_profile = models.CharField(max_length=100, null=True, blank=True) # OPTIONAL: Link to user's Instagram profile
    facebook_profile = models.CharField(max_length=100, null=True, blank=True) # OPTIONAL: Link to user's Facebook profile
    twitch_profile = models.CharField(max_length=100, null=True, blank=True) # OPTIONAL: Link to user's Twitch profile
    personal_website = models.CharField(max_length=100, null=True, blank=True) # OPTIONAL: Link to user's personal website

    past_hackathons = models.ManyToManyField("Hackathon", blank=True) # OPTIONAL: A lit of past w3Hacks hackathons that the user has competed in
    projects = models.ManyToManyField("Project", blank=True) # List of projects created by user

    completed_project_exercises = models.ManyToManyField("CompletedProjectExercise", blank=True) # List of completed project exercises
    completed_quiz_exercises = models.ManyToManyField("CompletedQuizExercise", blank=True) # List of completed quiz exercises
    completed_fix_the_code_exercises = models.ManyToManyField("CompletedFixTheCodeExercise", blank=True) # List of completed fix_the_code exercises
    completed_brainteaser_exercises = models.ManyToManyField("CompletedBrainTeaserExercise", blank=True) # List of completed brainteaser exercises
    completed_visualization_exercises = models.ManyToManyField("CompletedVisualizationExercise", blank=True) # List of completed visualization exercises
    completed_refactor_exercises = models.ManyToManyField("CompletedRefactorExercise", blank=True) # List of completed refactor exercises
    completed_teaching_exercises = models.ManyToManyField("CompletedTeachingExercise", blank=True) # List of completed teaching exercises
    completed_github_exercises = models.ManyToManyField("CompletedGitHubExercise", blank=True) # List of completed github exercises
    completed_research_exercises = models.ManyToManyField("CompletedResearchExercise", blank=True) # List of completed research exercises

    joined_date = models.DateField(default=date.today()) # The date when the user joined w3Hacks
    credits = models.IntegerField(default=0) # The number of credits the user has
    overall_ranking_points = models.IntegerField(default=0) # The overall ranking points the user has
    hackathon_ranking_points = models.IntegerField(default=0) # The hackathon ranking points the user has
    project_ranking_points = models.IntegerField(default=0) # The project ranking points the user has
    quiz_ranking_points = models.IntegerField(default=0) # The quiz ranking points the user has
    exercise_ranking_points = models.IntegerField(default=0) # The exercise ranking points the user has

    def __str__(self):
        return self.user.username


# Project model for each project
class Project(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for project
    title = models.CharField(max_length=50) # Name of the project
    description = models.TextField(max_length=500) # Description of the project
    project_image = models.ImageField(null=True, blank=True) # OPTIONAL: Image of the project
    technologies_used = ArrayField(models.CharField(max_length=30), null=True, blank=True) # OPTIONAL: Array of technologies used for the project
    github_link = models.CharField(max_length=200, null=True, blank=True) # OPTIONAL: Link to the project on GitHub
    project_link = models.CharField(max_length=200, null=True, blank=True) # OPTIONAL: Link to the project if hosted on the app store or Internet
    video_link = models.CharField(max_length=200, null=True, blank=True) # OPTIONAL: Link to a video of project demo
    extra_files = ArrayField(models.FileField(), null=True, blank=True) # OPTIONAL: Array of extra files to submit along with project
    creator = models.ForeignKey("Profile", on_delete=models.PROTECT) # Creator of project
    likes = models.IntegerField(null=True, default=0) # Number of likes on project

    def __str__(self):
        return self.title


# Model for each hackathon, current or not
class Hackathon(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # ID for display
    title = models.CharField(max_length=50) # Name of the hackathon
    description = models.TextField(max_length=300) # Description of the hackathon
    start_datetime = models.DateTimeField() # Starting datetime for the hackathon
    end_datetime = models.DateTimeField() # Ending datetime for the hackathon
    submissions_open_datetime = models.DateTimeField() # Opening datetime for the submissions
    submissions_close_datetime = models.DateTimeField() # Closing datetime for the submissions
    winners_announced = models.DateTimeField() # Datetime to announce winners
    schedule = models.ManyToManyField("ScheduleEvent", blank=True) # List of ScheduleEvents for hackathon
    themes = models.ManyToManyField("Theme", blank=True) # List of themes for hackathon
    awards = models.ManyToManyField("Award", blank=True) # List of awards for hackathon
    resources = models.ManyToManyField("ResourceLink", blank=True) # List of resource links for hackathon
    competitors = models.ManyToManyField("Profile", blank=True) # List of competitor profiles; can be empty in beginning
    submissions = models.ManyToManyField("Project", blank=True) # List of project submissions; can be empty in beginning

    def __str__(self):
        return self.title


#############################################################################################################################


####################
## PROFILE MODELS ##
####################

# For 'Themes' section of Hackathon
class Theme(models.Model):
    title = models.CharField(max_length=50) # Name of the theme
    description = models.TextField(max_length=300) # Description of the theme

    def __str__(self):
        return self.title


#############################################################################################################################


#####################
## EXERCISE MODELS ##
#####################

class Topic(models.Model):
    name = models.CharField(max_length=50) # Name of the topic
    searchable_name = models.CharField(max_length=50) # Name of the topic that will be added into the query parameter
    image = models.ImageField() # Image for the topic

    def __str__(self):
        return self.name


class DifficultyLevel(models.Model):
    name = models.CharField(max_length=50) # Name of the difficulty level (easy, medium, hard)
    searchable_name = models.CharField(max_length=50) # Name of the difficulty level that will be added into the query parameter

    def __str__(self):
        return self.name


####################
## PROJECT MODELS ##
####################

class ProjectExercise(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for project exercises
    name = models.CharField(max_length=50) # Name of the project
    description = models.TextField() # Description of the project
    topic = models.ForeignKey("Topic", on_delete=models.PROTECT) # The topic of the exercise
    difficulty_level = models.ForeignKey("DifficultyLevel", on_delete=models.PROTECT) # The difficulty level of the exercise
    prerequisites = ArrayField(models.CharField(max_length=50), null=True, blank=True) # List of string prerequisites needed for this project
    resources = models.ManyToManyField("ResourceLink", blank=True) # Resources for this project

    def __str__(self):
        return self.name


class CompletedProjectExercise(models.Model):
    project_exercise = models.ForeignKey("ProjectExercise", on_delete=models.PROTECT) # The project completed
    github_link = models.CharField(max_length=100) # Link to GitHub repo
    score = models.IntegerField(null=True, blank=True) # Score for how good the project is from 1-10

    def __str__(self):
        return "Completed Project Exercise: " + self.project_exercise.name


#################
## QUIZ MODELS ##
#################

class QuizExercise(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for quiz exercise
    name = models.CharField(max_length=50) # Name of the quiz
    description = models.TextField() # Description of the quiz
    topic = models.ForeignKey("Topic", on_delete=models.PROTECT) # The topic of the exercise
    difficulty_level = models.ForeignKey("DifficultyLevel", on_delete=models.PROTECT) # The difficulty level of the exercise
    prerequisites = ArrayField(models.CharField(max_length=50), null=True, blank=True) # List of string prerequisites needed for this quiz
    resources = models.ManyToManyField("ResourceLink", blank=True) # Resources for this quiz
    questions = models.ManyToManyField("QuizQuestion") # Questions for this quiz

    def __str__(self):
        return self.name


# For the QuizExercise model
class QuizQuestion(models.Model):
    question = models.CharField(max_length=100) # The question
    answers = ArrayField(models.CharField(max_length=100)) # Array of possible answers
    correct_answer_index = models.IntegerField() # Index of the correct answer in 'answers' field of this model
    question_image = models.ImageField(null=True, blank=True) # Image for the question

    def __str__(self):
        return self.question


class CompletedQuizExercise(models.Model):
    quiz_exercise = models.ForeignKey("QuizExercise", on_delete=models.PROTECT) # The quiz taken
    answers = ArrayField(models.CharField(max_length=100)) # Answers provided by the user
    number_of_correct_answers = models.IntegerField() # Number of questions the user got correct
    number_of_questions = models.IntegerField() # Number of questions in the quiz

    def __str__(self):
        return "Completed Quiz Exercise: " + self.quiz_exercise.name


##########################
## MINI-EXERCISE MODELS ##
##########################

class MiniExercise(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for mini-exercise
    name = models.CharField(max_length=50) # Name of the mini exercise
    description = models.TextField() # Description of the mini exercise
    topic = models.ForeignKey("Topic", on_delete=models.PROTECT) # The topic of the exercise
    difficulty_level = models.ForeignKey("DifficultyLevel", on_delete=models.PROTECT) # The difficulty level of the exercise
    prerequisites = ArrayField(models.CharField(max_length=50), null=True, blank=True) # List of string prerequisites needed for this mini exercise
    resources = models.ManyToManyField("ResourceLink", blank=True) # Resources for this mini exercise

    def __str__(self):
        return self.name


class FixTheCodeExercise(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for fix the code mini-exercise
    name = models.CharField(max_length=50) # Name of the fix the code mini exercise
    description = models.TextField() # Description of the fix the code mini exercise
    topic = models.ForeignKey("Topic", on_delete=models.PROTECT) # The topic of the exercise
    difficulty_level = models.ForeignKey("DifficultyLevel", on_delete=models.PROTECT) # The difficulty level of the exercise
    prerequisites = ArrayField(models.CharField(max_length=50), null=True, blank=True) # List of string prerequisites needed for this fix the code mini exercise
    resources = models.ManyToManyField("ResourceLink", blank=True) # Resources for this fix the code mini exercise
    repl_link = models.CharField(max_length=100) # Link to repl.it the user will use

    def __str__(self):
        return self.name


class CompletedFixTheCodeExercise(models.Model):
    fix_the_code_exercise = models.ForeignKey("FixTheCodeExercise", on_delete=models.PROTECT) # The mini exercise taken
    repl_link = models.CharField(max_length=100) # Link to completed repl
    score = models.IntegerField(null=True, blank=True) # Score for how good the mini exercise completion is from 1-10

    def __str__(self):
        return "Completed Fix the Code Exercise: " + self.fix_the_code_exercise.name


class BrainTeaserExercise(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for the mini-exercise
    name = models.CharField(max_length=50) # Name of the mini exercise
    description = models.TextField() # Description of the mini exercise
    topic = models.ForeignKey("Topic", on_delete=models.PROTECT) # The topic of the exercise
    difficulty_level = models.ForeignKey("DifficultyLevel", on_delete=models.PROTECT) # The difficulty level of the exercise
    prerequisites = ArrayField(models.CharField(max_length=50), null=True, blank=True) # List of string prerequisites needed for this mini exercise
    resources = models.ManyToManyField("ResourceLink", blank=True) # Resources for this mini exercise
    repl_link = models.CharField(max_length=100) # Link to the repl the user will use

    def __str__(self):
        return self.name


class CompletedBrainTeaserExercise(models.Model):
    brainteaser_exercise = models.ForeignKey("BrainTeaserExercise", on_delete=models.PROTECT) # The mini exercise taken
    repl_link = models.CharField(max_length=100) # Link to completed repl
    score = models.IntegerField(null=True, blank=True) # Score for how good the mini exercise completion is from 1-10

    def __str__(self):
        return "Completed Brain Teaser Exercise: " + self.brainteaser_exercise.name


class RefactorExercise(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for the mini-exercise
    name = models.CharField(max_length=50) # Name of the mini exercise
    description = models.TextField() # Description of the mini exercise
    topic = models.ForeignKey("Topic", on_delete=models.PROTECT) # The topic of the exercise
    difficulty_level = models.ForeignKey("DifficultyLevel", on_delete=models.PROTECT) # The difficulty level of the exercise
    prerequisites = ArrayField(models.CharField(max_length=50), null=True, blank=True) # List of string prerequisites needed for this mini exercise
    resources = models.ManyToManyField("ResourceLink", blank=True) # Resources for this mini exercise
    repl_link = models.CharField(max_length=100) # Link to the repl the user will use

    def __str__(self):
        return self.name


class CompletedRefactorExercise(models.Model):
    refactor_exercise = models.ForeignKey("RefactorExercise", on_delete=models.PROTECT) # The mini exercise taken
    repl_link = models.CharField(max_length=100) # Link to completed repl
    score = models.IntegerField(null=True, blank=True) # Score for how good the mini exercise completion is from 1-10

    def __str__(self):
        return "Completed Refactor Exercise: " + self.refactor_exercise.name


class VisualizationExercise(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for the mini-exercise
    name = models.CharField(max_length=50) # Name of the mini exercise
    description = models.TextField() # Description of the mini exercise
    topic = models.ForeignKey("Topic", on_delete=models.PROTECT) # The topic of the exercise
    difficulty_level = models.ForeignKey("DifficultyLevel", on_delete=models.PROTECT) # The difficulty level of the exercise
    prerequisites = ArrayField(models.CharField(max_length=50), null=True, blank=True) # List of string prerequisites needed for this mini exercise
    resources = models.ManyToManyField("ResourceLink", blank=True) # Resources for this mini exercise

    def __str__(self):
        return self.name


class CompletedVisualizationExercise(models.Model):
    visualization_exercise = models.ForeignKey("VisualizationExercise", on_delete=models.PROTECT) # The mini exercise taken
    visualization_file = models.FileField() # File for draw.io visualization
    score = models.IntegerField(null=True, blank=True) # Score for how good the mini exercise completion is from 1-10

    def __str__(self):
        return "Completed Visualization Exercise: " + self.visualization_exercise.name


class TeachingExercise(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for the mini-exercise
    name = models.CharField(max_length=50) # Name of the mini exercise
    description = models.TextField() # Description of the mini exercise
    topic = models.ForeignKey("Topic", on_delete=models.PROTECT) # The topic of the exercise
    difficulty_level = models.ForeignKey("DifficultyLevel", on_delete=models.PROTECT) # The difficulty level of the exercise
    formats = ArrayField(models.CharField(max_length=50), null=True, blank=True) # The formats available to submit (Video, Document)
    prerequisites = ArrayField(models.CharField(max_length=50), null=True, blank=True) # List of string prerequisites needed for this mini exercise
    resources = models.ManyToManyField("ResourceLink", blank=True) # Resources for this mini exercise

    def __str__(self):
        return self.name


class CompletedTeachingExercise(models.Model):
    teaching_exercise = models.ForeignKey("TeachingExercise", on_delete=models.PROTECT) # The mini exercise taken
    teaching_exercise_link = models.CharField(max_length=200) # Link to completed exercise (YouTube video, Google Docs link)
    score = models.IntegerField(null=True, blank=True) # Score for how good the mini exercise completion is from 1-10

    def __str__(self):
        return "Completed Teaching Exercise: " + self.teaching_exercise.name


class GitHubExercise(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for the mini-exercise
    name = models.CharField(max_length=50) # Name of the mini exercise
    description = models.TextField() # Description of the mini exercise
    topic = models.ForeignKey("Topic", on_delete=models.PROTECT) # The topic of the exercise
    difficulty_level = models.ForeignKey("DifficultyLevel", on_delete=models.PROTECT) # The difficulty level of the exercise
    prerequisites = ArrayField(models.CharField(max_length=50), null=True, blank=True) # List of string prerequisites needed for this mini exercise
    resources = models.ManyToManyField("ResourceLink", blank=True) # Resources for this mini exercise

    def __str__(self):
        return self.name


class CompletedGitHubExercise(models.Model):
    github_exercise = models.ForeignKey("GitHubExercise", on_delete=models.PROTECT) # The mini exercise taken
    github_exercise_link = models.CharField(max_length=200) # Link to completed exercise (PR or Issue link)
    score = models.IntegerField(null=True, blank=True) # Score for how good the mini exercise completion is from 1-10

    def __str__(self):
        return "Completed GitHub Exercise: " + self.github_exercise.name


class ResearchExercise(models.Model):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=generate_id) # Unique ID for the mini-exercise
    name = models.CharField(max_length=50) # Name of the mini exercise
    description = models.TextField() # Description of the mini exercise
    topic = models.ForeignKey("Topic", on_delete=models.PROTECT) # The topic of the exercise
    difficulty_level = models.ForeignKey("DifficultyLevel", on_delete=models.PROTECT) # The difficulty level of the exercise
    prerequisites = ArrayField(models.CharField(max_length=50), null=True, blank=True) # List of string prerequisites needed for this mini exercise
    resources = models.ManyToManyField("ResourceLink", blank=True) # Resources for this mini exercise
    error = models.TextField(null=True, blank=True) # OPTIONAL: Error to research about

    def __str__(self):
        return self.name


class CompletedResearchExercise(models.Model):
    research_exercise = models.ForeignKey("ResearchExercise", on_delete=models.PROTECT) # The mini exercise taken
    research_link = models.CharField(max_length=200) # Link to completed exercise (StackOverflow or documentation link)
    score = models.IntegerField(null=True, blank=True) # Score for how good the mini exercise completion is from 1-10

    def __str__(self):
        return "Completed Research Exercise: " + self.research_exercise.name


# For 'Resources' section of Hackathon
class ResourceLink(models.Model):
    title = models.CharField(max_length=50) # String to be shown on display
    url_extension = models.CharField(max_length=50, unique=True) # String for url extension
    link = models.CharField(max_length=200) # Actual link URL

    def __str__(self):
        return self.title


#############################################################################################################################


######################
## HACKATHON MODELS ##
######################

# For each award for Hackathon
class Award(models.Model):
    title = models.CharField(max_length=50) # Name of the award
    description = models.TextField(max_length=300) # Description of the award
    prize = models.CharField(max_length=100) # Prize for the winner of the award
    winner = models.ForeignKey("Profile", on_delete=models.PROTECT, null=True, blank=True) # Winner of the award

    def __str__(self):
        return self.title


# For each event on Hackathon schedule
class ScheduleEvent(models.Model):
    title = models.CharField(max_length=50) # Name of the event
    description = models.TextField(max_length=300) # Description of the event
    scheduled_datetime = models.DateTimeField(null=True, blank=True) # When the event is scheduled
    event_link = models.ForeignKey("ResourceLink", on_delete=models.CASCADE, null=True, blank=True) # OPTIONAL: Link for the event

    def __str__(self):
        return self.title
