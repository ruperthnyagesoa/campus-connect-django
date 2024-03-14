from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post, Follow, Like
from datetime import datetime
from django.shortcuts import get_object_or_404

from django.contrib.staticfiles import finders
import os
import openai

openai.api_key = "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"



def index(request):
    if request.method == "POST":
        message = 'Character length must be more than 3!'
        new_post = request.POST["new_post"]
        d = datetime.now()
        posts = Post(text=new_post, user=request.user, created_at=d.strftime("%b %d, %Y, %I:%M %p"))
        if posts.is_content_valid() == False:
            return render(request, "network/index.html", {"message": message})
        posts.save()
        return redirect("index")
    
    else:
        #orders by created_at which is the time. the - before the created_at signifies descending order 
        posts = Post.objects.order_by("-created_at") 
        #user_like = request.user.id
        likes = Like.objects.all()
        liked = Like.objects.filter(user_id=request.user.id)
        liked_post_ids = [like.post_id for like in liked]
        likes_count = likes.count()
        return render(request, "network/index.html", {"posts": posts, "likes_count": likes_count, "likes":likes, "liked_post_ids":liked_post_ids,})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def profile(request, id):
    try:
        if request.method == "POST":
            profile = User.objects.get(pk=id)
            date = datetime.now()
            #TODO: update the below code if successfully done in JavaScript
            follower = Follow(follower=request.user, following=profile, follower_date=date.strftime("%b %d, %Y, %I:%M %p"))
            follower.save()
            follower.number_of_followers()
            return JsonResponse({'success': True})
        else:
            profile = User.objects.get(pk=id)
            posts = Post.objects.all().filter(user=profile)
            followings = Follow.objects.all().filter(follower=request.user, following=profile).exists()
            follow = Follow.objects.all().filter(follower=request.user, following=profile)
            followers = Follow.objects.all().filter(following=profile)
            following = Follow.objects.all().filter(follower=profile)
            num_followers = Follow.number_of_followers()


            return render(request, "network/profile.html", {"posts":posts, "profile":profile, "followings":followings, "followers":num_followers})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def unfollow(request, id):
    try:
        if request.method == "POST":
            profile = User.objects.get(pk=id)
            #TODO: update the below code if successfully done in JavaScript
            follower = Follow.objects.filter(follower=request.user, following=profile)
            follower.delete()
            return JsonResponse({'success': True})
        else:
            #unfollow = ''
            profile = User.objects.get(pk=id)
            posts = Post.objects.all().filter(user=profile)
            followings = Follow.objects.all().filter(follower=request.user, following=profile).exists()
            followers = Follow.objects.all().filter(following=profile)
            following = Follow.objects.all().filter(follower=profile)
          
           
            return render(request, "network/profile.html", {"posts":posts, "profile":profile, "followings":followings, "followers":followers.count(), "following":following.count()})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def edit(request, id):
    if request.method == "POST":
        post = Post.objects.get(pk=id)
        content = request.POST['new_post']
        post.text = content
        post.save()
        return redirect("index")
    else:
        post = Post.objects.get(pk=id)  
        posts = Post.objects.filter(pk=post.pk, user=request.user)
        return render(request, "network/edit.html", {"posts": posts})
    
def following(request):

    follow_objects = Follow.objects.filter(follower=request.user)

    following_users = []
    for follow_object in follow_objects:
        following_users.append(follow_object.following)

    posts = Post.objects.filter(user__in=following_users).order_by("-created_at")

    return render(request, "network/following.html", {"posts": posts})

def like(request, id):
    try:
        if request.method == "POST":
            post = Post.objects.get(pk=id)
            date = datetime.now()
            likes = Like(post=post, user=request.user, like_date=date.strftime("%b %d, %Y, %I:%M %p"))
            likes.save()
            return JsonResponse({'success': True})
        
        else:
            post = Post.objects.get(pk=id)
            likes = Like.objects.all().filter(post=post)
            return redirect("index")
                
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def class_ai(request):
    if request.method == "POST":
        question = request.POST["question"]
        document = ''
        
        try:
            file_path = finders.find('network/solomon.txt')
            with open(file_path) as file:
                document = file.read()
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        prompt = f"""Your task is to answer the following questions accurately about Solomon:
        {question}
    
        Answer the questions only from the text delimited by triple backticks:

        Text: ```{document}```

        if question is not found in the document, answer with "I don't know, I'm sorry!" or "I'm sorry, I don't have the knowledge of that"
         
        Answer the questions with no more than 10 words. 

        Just answer the question only without repeating the question.
        """
        response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,
                    max_tokens=100,
                    n=1,
                    stop=None,
                    temperature=0.4,
        )

        answer = response.choices[0].text.strip()

        return render(request, "network/class.html", {"question":question, "answer":answer}) 


    else: 
        return render(request, "network/class.html", {})


