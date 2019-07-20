from django.shortcuts import render, redirect
from .models import Restaurant, Item
from .forms import RestaurantForm, SignupForm, SigninForm, CreateItemForm
from django.contrib.auth import login, authenticate, logout

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("restaurant-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('restaurant-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")

def restaurant_list(request):
    context = {
        "restaurants":Restaurant.objects.all()
    }
    return render(request, 'list.html', context)


def restaurant_detail(request, restaurant_id):
    cucumber = Restaurant.objects.get(id=restaurant_id)
# 
    context = {
        "restaurant": cucumber,
        "items": Item.objects.filter(restaurant=cucumber)
    }
    return render(request, 'detail.html', context)

def restaurant_create(request):
    form = RestaurantForm()
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.owner = request.user
            #                   ^^ this allows us to save the form under the user thats signed in form.owner
            form.save()
            #        ^^this saves the entry to the database
            return redirect('restaurant-list')
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)

def item_create(request, restaurant_id):
    form = CreateItemForm()
    potato = Restaurant.objects.get(id=restaurant_id)
    # ^^ this is like a cabinet for us to put the restaurant to which we want to save the items
    if request.method == "POST":
        form = CreateItemForm(request.POST, request.FILES)
        if form.is_valid():
            carrotcake = form.save(commit=False)
            carrotcake.restaurant = potato
            #                   ^^ this manually assigns the restraurant field to the POTATO variable
            carrotcake.save()
            # ^^ this is the SAVE function in Django.. now our info is saved in the database
            return redirect('restaurant-detail', restaurant_id)

    context = {
         "form":form,
         "potato_id": restaurant_id
    }
    return render(request, 'item_create.html', context)

def restaurant_update(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)
    form = RestaurantForm(instance=restaurant_obj)
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant_obj)
        if form.is_valid():
            form.save()
            return redirect('restaurant-list')
    context = {
        "restaurant_obj": restaurant_obj,
        "form":form,
    }
    return render(request, 'update.html', context)

def restaurant_delete(request, restaurant_id):
    restaurant_obj = Restaurant.objects.get(id=restaurant_id)
    restaurant_obj.delete()
    return redirect('restaurant-list')
