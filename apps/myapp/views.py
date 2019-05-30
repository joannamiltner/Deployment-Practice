from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages 
import bcrypt
# Destination.objects.all().delete()

def index(request):
    return render(request, 'index.html')


def createuser(request):
    errors = User.objects.regValidator(request.POST)
    print(errors)
    if errors:
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, key)
        return redirect("/")
    else:
        password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=password_hash.decode())
        request.session['id'] = user.id 
        return redirect("/traveldashboard")

def traveldashboard(request):
    if 'id' in request.session:
        print("Logged In")
        print(request.session['id'])
        user = User.objects.get(id=request.session['id'])
        destinations = Destination.objects.all()
        joins = Join.objects.filter(user_id=request.session['id'])
        notFavs = []
        favs = []

        for join in joins:
            favs.append(join.destination_id)
        print(favs)
        for destination in destinations:
            if destination.id not in favs:
                notFavs.append(destination)
        print(notFavs)
        
        context = {
            "user": user,
            "destinations": destinations,
            "joins": joins,
            "notFavs": notFavs
        }
        return render(request, 'traveldashboard.html', context)
    else:
        print(request.session['id'])
        return redirect("/")
    
def favorite(request, destination_id):
    Join.objects.create(destination_id=destination_id, user_id=request.session['id'])
    return redirect("/traveldashboard")

def login(request):
    errors = User.objects.loginValidator(request.POST)
    print(errors)
    if errors:
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, key)
        return redirect("/")
    else:
        users = User.objects.filter(username=request.POST['username'])
        request.session['id'] = users[0].id
    return redirect("/traveldashboard")

def create_trip(request):
    errors = Destination.objects.destinationValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, key)
        return redirect("/add")
    else:
        destination = Destination.objects.create(city=request.POST['city'], destination_description=request.POST['destination_description'], start_date=request.POST['start_date'], end_date=request.POST['end_date'],added_by_id=request.session['id'])
        Join.objects.create(destination=destination, user_id=request.session['id'])
        print()
        return redirect("/traveldashboard")
        
    
def add(request):
    return render(request, 'add.html')

def description(request, destination_id):
    context = {
        "destination": Destination.objects.get(id=destination_id),
        "users_who_fave_destination": Join.objects.filter(destination_id=destination_id)
    }
    return render(request, 'description.html', context)


def logout(request):
    request.session.clear()
    print("Logged Out")
    return redirect("/")