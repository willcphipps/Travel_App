import bcrypt
from django.shortcuts import render, redirect
from .models import Users, Destinations
from django.contrib import messages


def index(request):
    
    return render(request, 'index.html')

def register(request):
    errors = Users.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='registration')
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = Users.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash)
        request.session['userid'] = user.id
    return redirect('/dashboard')


def login(request):
    errors = Users.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value, in errors.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    else:
        user = Users.objects.filter(email=request.POST['email'])
        logged_user = user[0]
        request.session['userid'] = logged_user.id
        return redirect('/dashboard')


def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'userid' in request.session:
        others = Destinations.objects.exclude(trip_admin=Users.objects.get(id=request.session['userid']))
        trips = Destinations.objects.filter(travelers=Users.objects.get(id=request.session['userid']))
        context = {
            'user': Users.objects.get(id=request.session['userid']),
            'my_trips': trips,
            'other_trips': others.exclude(travelers=Users.objects.get(id=request.session['userid']))
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

def new_trip(request):
    if 'userid' in request.session:
        context = {
            'user' : Users.objects.get(id=request.session['userid'])
        }
        return render(request, 'trips.html', context)
    else:
        return redirect('/')

def add_new(request):
    errors = Destinations.objects.add_new_validator(request.POST)
    if 'userid' in request.session:
        if len(errors) > 0:
            for key, value, in errors.items():
                messages.error(request, value, extra_tags='new_destination')
            return redirect('/trips/new')
        else:
            place = Destinations.objects.create(destination=request.POST['destination'], start_date=request.POST['start'], end_date=request.POST['end'], plan=request.POST['plan'], trip_admin=Users.objects.get(id=request.session['userid'],))
            place.travelers.add(Users.objects.get(id=request.session['userid']))
            return redirect('/dashboard')
    else:
        return redirect('/')

def edit(request, trip_id):
    if 'userid' in request.session:
        context = {
            'user': Users.objects.get(id=request.session['userid']),
            'trip' : Destinations.objects.get(id=trip_id)
        }
        return render(request, 'edit.html', context)
    else:
        return redirect('/')

def show(request, trip_id):
    if 'userid' in request.session:
        context = {
            'traveler' : Users.objects.filter(joined_trips=Destinations.objects.get(id=trip_id)),
            'user': Users.objects.get(id=request.session['userid']),
            'trip' : Destinations.objects.get(id=trip_id)
        }
        return render(request, 'show.html', context)
    else:
        return redirect('/')

def join(request, trip_id):
    if 'userid' in request.session:
        user = Users.objects.get(id=request.session['userid']),
        # print(user)
        traveler = user[0]
        trip = Destinations.objects.get(id=trip_id)
        if traveler.id != trip.trip_admin.id:
            trip.travelers.add(traveler)
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')
    else:
        return redirect('/')
    

def update(request):
    errors = Destinations.objects.add_new_validator(request.POST)
    if 'userid' in request.session:
        if len(errors) > 0:
            for key, value, in errors.items():
                messages.error(request, value, extra_tags='edit_destination')
                trip_id = request.POST['trip_id']
            return redirect(f'/trips/edit/{trip_id}')
        else:
            update_trip = Destinations.objects.get(id=request.POST['trip_id'])
            update_trip.destination = request.POST['destination']
            update_trip.start_date = request.POST['start']
            update_trip.end_date = request.POST['end']
            update_trip.plan = request.POST['plan']
            update_trip.save()
            
            return redirect('/dashboard')
    else:
        return redirect('/')



def remove(request, trip_id):
    if 'userid' in request.session:
        Destinations.objects.get(id=trip_id).delete()
        return redirect('/dashboard')
    else:
        return redirect('/')

# class Destinations(models.Model):
#     trip_admin = models.ForeignKey(Users, related_name="created_trips", on_delete=models.CASCADE)
#     destination = models.CharField(max_length=45)
#     start_date = models.CharField(max_length=45)
#     end_date = models.CharField(max_length=45)
#     plan = models.CharField(max_length=200)
#     travelers = models.ManyToManyField(Users, related_name="joined_trips")
#     objects = DestinationsManager()
