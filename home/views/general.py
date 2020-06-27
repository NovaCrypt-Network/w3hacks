from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from main import models
from datetime import datetime, date
import json


def generate_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])

def handler404(request, *args, **argv):
    return render(request, "errors/404.html")

def handler500(request, *args, **argv):
    return render(request, "errors/500.html")


def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email_body = f"From: {name}\nEmail: {email}\n\n{message}"
        EmailMessage("w3Hacks Contact Us", email_body, to=["calix.huang1@gmail.com"]).send()

        return render(request, "home/index.html", context={
            "message": "Message sent!"
        })

    if request.user.is_authenticated:
        return render(request, "home/index.html")
    else:
        return render(request, "home/landingpage.html")


def contact(request):
    return render(request, "home/contact.html")


from djstripe.models import Product
import stripe
from django.conf import settings

def pricing(request):
    return render(request, "home/pricing.html", context={
        "products": Product.objects.all()
    })

@login_required
def create_customer_and_subscription(request):
    """
    Create a Stripe Customer and Subscription object and map them onto the User object
    Expects the inbound POST data to look something like this:
    {
        'email': 'cory@saaspegasus.com',
        'payment_method': 'pm_1GGgzaIXTEadrB0y0tthO3UH',
        'plan_id': 'plan_GqvXkzAvxlF0wR',
    }
    """
    # parse request, extract details, and verify assumptions
    request_body = request.POST
    email = request_body['email']
    assert request.user.email == email
    payment_method = request_body['payment_method']
    plan_id = request_body['plan_id']
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # first sync payment method to local DB to workaround
    # https://github.com/dj-stripe/dj-stripe/issues/1125
    payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
    djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

    # create customer objects
    # This creates a new Customer in stripe and attaches the default PaymentMethod in one API call.
    customer = stripe.Customer.create(
      payment_method=payment_method,
      email=email,
      invoice_settings={
        'default_payment_method': payment_method,
      },
    )
    djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)

    # create subscription
    subscription = stripe.Subscription.create(
      customer=customer.id,
      items=[
        {
          'plan': plan_id,
        },
      ],
      expand=['latest_invoice.payment_intent'],
    )
    djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

    # associate customer and subscription with the user
    request.user.customer = djstripe_customer
    request.user.subscription = djstripe_subscription
    request.user.save()

    # return information back to the front end
    data = {
        'customer': customer,
        'subscription': subscription
    }
    return JsonResponse(
        data=data,
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticating user
        user = authenticate(username=username, password=password)

        if user: # Valid credentials
            if user.is_active: # User is active
                # Log the user in
                login(request, user)
                return HttpResponseRedirect("/")

            else: # User has an inactive account
                # Re-render page with error message
                return render(request, "home/login.html", context={
                    "message": "User account has been deactivated. Please register again.",
                    "status": "bad"
                })

        else: # Invalid credentials
            # Re-render page with error message
            return render(request, "home/login.html", context={
                "message": "Invalid credentials.",
                "status": "bad"
            })

    return render(request, "home/login.html")


def register(request):
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
        location = request.POST.get("location")
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

        # Creating the user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )
        user.set_password(password) # Setting the password separately for encryption

        # Creating the custom profile
        profile = models.Profile(
            user=user,
            biography=biography,
            location=location,
            education=education,
            skills=skills,
            github_profile=github_profile,
            linkedin_profile=linkedin_profile,
            twitter_profile=twitter_profile,
            instagram_profile=instagram_profile,
            facebook_profile=facebook_profile,
            twitch_profile=twitch_profile,
            personal_website=personal_website
        )

        # To avoid 'Invalid Date Format' error for empty birthday
        if birthday:
            profile.birthday = birthday

        # Checking if they provided picture
        if 'profile-picture' in request.FILES:
            profile.profile_picture = request.FILES['profile-picture']


        # Only save models when no errors have blocked registration
        try:
            user.save()
            profile.save()
        except IntegrityError:
            return render(request, "home/register.html", context={
                "message": "Username and/or email is already taken. Please double check.",
                "status": "bad",
                "today": str(date.today())
            })


        login(request, user) # Logging the user in

        return HttpResponseRedirect("/")

    return render(request, "home/register.html", context={
        "today": str(date.today())
    })

import stripe
stripe.api_key = '		sk_test_51Gsz1LJ09tuJBIN8ddJzUkQVXasV78S53uCYVBPbyi57RWhIbvdIsoWYZqZpQyEOAYy4h21aBrJkGqDkCexk3Jto00YQ08b88v'

def test_register(request):
    return render(request, "home/test-register2.html")

def create_customer(request):
    print("create customer")
    try:
        customer = stripe.Customer.create(
            email=request.POST.get("email")
        )
        print(customer)
        return JsonResponse(customer)
    except Exception as e:
        return JsonResponse(e)

def create_subscription(request):
    print("create subscription")
    if request.method == "POST":
        try:
            # Attach the payment method to the customer
            stripe.PaymentMethod.attach(
                request.POST.get("paymentMethodId"),
                customer=request.POST.get("customerId"),
            )
            # Set the default payment method on the customer
            stripe.Customer.modify(
                request.POST.get("customerId"),
                invoice_settings={
                    'default_payment_method': request.POST.get("paymentMethodId"),
                },
            )

            # Create the subscription
            subscription = stripe.Subscription.create(
                customer=request.POST.get("paymentMethodId"),
                items=[
                    {
                        'price': 'price_1GszrXJ09tuJBIN8nkxZgFMK'
                    }
                ],
                expand=['latest_invoice.payment_intent'],
            )

            print(subscription)

            return JsonResponse(subscription)
        except Exception as e:
            return JsonResponse(e)

def retry_invoice(request):
    try:
        stripe.PaymentMethod.attach(
            request.POST.get("paymentMethodId"),
            customer=request.POST.get("customerId"),
        )
        # Set the default payment method on the customer
        stripe.Customer.modify(
            request.POST.get("customerId"),
            invoice_settings={
                'default_payment_method': request.POST.get("paymentMethodId"),
            },
        )

        invoice = stripe.Invoice.retrieve(
            request.POST.get("invoiceId"),
            expand=['payment_intent'],
        )

        return JsonResponse(invoice)
    except Exception as e:
        return JsonResponse(e)

def cancel_subscription(request):
    data = request.POST
    try:
        deletedSubscription = stripe.Subscription.delete(data.get("subscriptionId"))
        return JsonResponse(deletedSubscription)
    except Exception as e:
        return JsonResponse(e)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url="http://www.w3hacks.com/login")
def leaderboards(request):
    all_profiles = models.Profile.objects.all()

    overall_rankings = sorted(all_profiles, key=lambda x: x.overall_ranking_points)
    project_rankings = sorted(all_profiles, key=lambda x: x.project_ranking_points)
    quiz_rankings = sorted(all_profiles, key=lambda x: x.quiz_ranking_points)
    exercise_rankings = sorted(all_profiles, key=lambda x: x.exercise_ranking_points)

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Leaderboards", "link": "/leaderboards/"}
    ]

    return render(request, "home/leaderboards.html", context={
        "overall_rankings": overall_rankings,
        "project_rankings": project_rankings,
        "quiz_rankings": quiz_rankings,
        "exercise_rankings": exercise_rankings,
        "breadcrumbs": breadcrumbs
    })


# Activities views
@login_required(login_url="http://www.w3hacks.com/login")
def exercises(request):
    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/"}
    ]

    return render(request, "home/exercises/exercises.html", context={
        "breadcrumbs": breadcrumbs
    })


# Hackathon views
@login_required(login_url="http://www.w3hacks.com/login")
def about_the_hackathon(request):
    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "About The Hackathon", "link": "/about-the-hackathon/"}
    ]

    return render(request, "home/hackathon/about-the-hackathon.html", context={
        "breadcrumbs": breadcrumbs
    })


@login_required(login_url="http://www.w3hacks.com/login")
def past_hackathons(request):
    all_hackathons = models.Hackathon.objects.all()

    past_hackathons = []
    for hackathon in all_hackathons:
        # Hackathon end date was less than today
        if hackathon.end_datetime.strftime("%d/%m/%Y %H:%M:%S") < datetime.now().strftime("%d/%m/%Y %H:%M:%S"):
            past_hackathons.append(hackathon)

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Past Hackathons", "link": "/past-hackathons/"}
    ]

    return render(request, "home/hackathon/past-hackathons.html", context={
        "past_hackathons": past_hackathons,
        "breadcrumbs": breadcrumbs
    })


@login_required(login_url="http://www.w3hacks.com/login")
def future_hackathons(request):
    all_hackathons = models.Hackathon.objects.all()

    future_hackathons = []
    for hackathon in all_hackathons:
        # Hackathon end date was less than today
        if hackathon.start_datetime.strftime("%d/%m/%Y %H:%M:%S") > datetime.now().strftime("%d/%m/%Y %H:%M:%S"):
            future_hackathons.append(hackathon)

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Future Hackathons", "link": "/future-hackathons/"}
    ]

    return render(request, "home/hackathon/future-hackathons.html", context={
        "future_hackathons": future_hackathons,
        "breadcrumbs": breadcrumbs
    })
