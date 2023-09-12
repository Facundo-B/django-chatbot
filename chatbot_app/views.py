from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
import openai

openai_api_key = "APIKEY"
openai.api_key = openai_api_key


def ask_openai(message):
    """Send message through OpenAI's API"""
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages= [{'role':'user', 'content':message}],
        max_tokens = 200,
        temperature = 0.4
    )
    answer = response.choice[0].text.strip()

# Create your views here.
def chatbot(request):
    print(request.user)
    if request.user.is_authenticated :
        user_chats = Chat.objects.filter(user=request.user)
    else:
        user_chats = None

    if request.method == 'POST':
        message = request.POST.get('message')
        test_answer = 'Hello! This is a test answer.'
        answer = test_answer
        #answer = ask_openai(message)
        chat = Chat(user=request.user, message=message, response=answer, created_at = timezone.now())
        chat.save()
        return JsonResponse({'message':message,'answer': answer })
    return render(request, 'chatbot.html', {'user_chats': user_chats})

def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_msg = "invalid username or password"
            return render(request, login.html, {'error_msg': error_msg})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            try:
                new_user = User.objects.create_user(username, email, password1)
                new_user.save()
                auth.login(request, new_user)
                return redirect('chatbot')
            except:
                error_msg = 'Error creating account'
                return render(request, register.html, {'error_msg': error_msg})
        else:
            error_msg = "Passwords do not match"
            return render(request, register.html, {'error_msg': error_msg})
    else:
        return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')