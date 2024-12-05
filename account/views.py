from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from . models import Relation,Profile
from home.models import Post
from django.views import View
from .forms import UserRegisterationForm, UserLoginForm, UserEditForm, ProfileEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class UserRegisterationView(View):
    
    def get(self, request):
        form = UserRegisterationForm()
        return render(request, 'account/register.html',{'form':form})

    def post(self, request):
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            # Create and save the user, hashing the password
            user = User(username=username, email=email)
            user.set_password(password)  # This hashes the password
            user.save()
            messages.success(request, 'user registered successfully!', 'success')
            return redirect('home:home')
        return render(request, 'account/register.html', {'form':form})
    
class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'account/login.html', {'form':form})
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                login(request, user)                
                messages.success(request, 'user login successfully!', 'success')
                print('login')
                return redirect('home:home')
            print('form is valid')
            print(user)
            return redirect('account:login')
        print('form not valid')
        return render(request, 'account/login.html', {'form':form})
    
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you loged out successfully', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        posts = Post.objects.filter(user=user)
        is_following = Relation.objects.filter(from_user=request.user, to_user=user).exists()
        # followers = user.followers.all().values_list('from_user', flat=True)
        # followings = user.followings.all().values_list('to_user', flat=True)
         # Fetch full User objects for followers and followings
        followers = User.objects.filter(followers__to_user=user)
        followings = User.objects.filter(followings__from_user=user)

        return render(request, 'account/profile.html', {
            'user': user,
            'posts':posts,
            'is_following': is_following,
            'followers': followers,
            'followings': followings,
        })
    
class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        
        profile, created = Profile.objects.get_or_create(user=request.user)

        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)
        return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)

        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!', 'success')
            return redirect('account:profile', user_id=request.user.id)

        return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
    
class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation:
            messages.error(request, 'you already following this user!', 'danger')
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, 'you followed this user!', 'success')
        return redirect('account:profile', user.id)
    
class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user', 'success')
        else:
            messages.error(request, 'you are not following this user', 'danger')
        return redirect('account:profile', user.id)