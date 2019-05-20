from django.contrib.auth import (
    authenticate, get_user_model, login, logout,
)
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, EditProfileForm ,ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from .forms import ChangeBasicInfo
from .models import UserProfile



def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("home")

    return render(request, "accounts/login.html", {"form":form, "title":title})


def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password1 = form.cleaned_data.get('password')
        user.set_password(password1)
        user.save()
        login(request, user)
        return redirect("/posts")

    context = {
        "form":form,
        "title":title,
    }
    return render(request, "accounts/register.html", context)



def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')

    else:
        form = EditProfileForm(instance=request.user)

    args = {'form': form}
    return render(request, 'accounts/edit_profile.html', args)




def edit_info(request):
    if request.method == 'POST':
        form = ChangeBasicInfo(request.POST,  request.FILES, instance=UserProfile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = ChangeBasicInfo(instance=UserProfile.objects.get(user=request.user))

    args = {'form': form}
    return render(request, 'accounts/edit_info.html', args)




def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)

        if form.is_valid():

            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/change-password')

    else:
        form = ChangePasswordForm(user=request.user)

    args = {'form': form}
    return render(request, 'accounts/change_password.html', args)




def logout_view(request):
    logout(request)
    return redirect("home")
