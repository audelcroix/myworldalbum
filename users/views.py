from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import *
from album.models import *
from .models import *



def register(request):
    context = {}
    context["title"] = "Register"
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        context["form"] = form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("photographer_home", kwargs={'slug':user.photographer.slug}))
            else:
                messages.error(request, f'We are sorry, an error occured')
            # return redirect('/')
    else:
        form = UserRegisterForm()
        context["form"] = form
    return render(request, 'users/register.html', context)


def photographer_connect(request):
    error = False
    title = "Login"
    if request.method == "POST":
        form = Connection_form(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("photographer_home", kwargs={'slug':user.photographer.slug}))
            else:
                error = True
                messages.error(request, "Wrong username or password")
                return redirect('login')

        else:
            messages.error(request, "Wrong username or password")
            return redirect('login')

    else:
        form = Connection_form()
        return render(request, 'users/login.html', locals())


@login_required
def profile_update(request, author_slug):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        photographer_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.photographer)

        current_image = Photographer.objects.get(pk=request.user.photographer.pk).image#.delete(save=True)
        # print(current_image)
        if user_form.is_valid() and photographer_form.is_valid():
            new_image = request.user.photographer.image
            if new_image and current_image.name != "profile_pics/default.jpg" and current_image.name != "default.jpg":
                current_image.delete(False)

            user_form.save()
            photographer_form.save()
            messages.success(request, f'Your profile has been successfully updated')
            return redirect(reverse("photographer_home", kwargs={'slug':request.user.photographer.slug}))

    else:
        user_form = UserUpdateForm(instance=request.user)
        photographer_form = ProfileUpdateForm(instance=request.user.photographer)

    context = {
        'user_form': user_form,
        'photographer_form': photographer_form,
        'title': 'Update'
    }

    return render(request, 'users/profile_update.html', context)


def UserProfileView(request, slug):
    photographer_info = get_object_or_404(Photographer, slug=slug)
    context = {
        'photographer_info':photographer_info,
        'photos': Photo.objects.filter(author=photographer_info)
    }

    return render(request, 'users/photographer_profile_home.html', context)


def about(request):
    context = {
        "title": "About"
    }

    return render(request, 'users/about.html', context)


@login_required
def UserPasswordUpdate(request, author_slug):

    if request.method == "POST":
        pass_update_form = PasswordUpdateForm(request.POST)

        if pass_update_form.is_valid():
            new_password = pass_update_form.cleaned_data["new_password"]
            old_password = pass_update_form.cleaned_data["old_password"]

            checked = request.user.check_password(old_password)
            if checked:
                request.user.set_password(new_password)
                request.user.save()
                # auto logout after password update, so user has to be logged in again
                update_session_auth_hash(request, request.user)
                messages.success(request, f'Your password has been successfully updated')

                return redirect(reverse("photographer_home", kwargs={'slug':user.photographer.slug}))
            else:
                messages.error(request, f'The given password is incorrect')

    else:
        pass_update_form = PasswordUpdateForm()

    context = {
        'pass_update_form': pass_update_form,
        'title': 'Password update'
    }

    return render(request, 'users/password_update.html', context)
