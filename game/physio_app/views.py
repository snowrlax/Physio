from pyexpat.errors import messages
from django.conf import settings
from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from physio_app.models import UserProfile, saveEmail, CustomUser
import json
import random
import os
import physio_app.flappygames  as game1
import physio_app.shoulder as game2
import physio_app.ping_pong as game3

import physio_app.newshoulder  as shoulder
import physio_app.leg  as leg
from django.http import StreamingHttpResponse
#-------------------ChatBot-----------------
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'intents1.json')
intents = open(file_path)
p = json.load(intents)
saved_username = ["You"]

class ChatInterface:
    def __init__(self):
        self.temp = ""
        self.z = 0

    def chat(self, input_str):
        responses = []
        input_list = input_str.split()
        po = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        if input_str == "start":
            return "Enter suger level and bp \n a = Blood Pressure (Low, Normal) \n b = Blood Pressure (High) \n c = Sugar Level (Low, Normal)  \n d = Sugar Level (High)"
        if input_str == 'a' or input_str == 'b' or input_str == 'c' or input_str == 'd':
            self.z = input_str
        print(self.z)

        for ip in input_list:   
            if ip in po:
                print(ip)

            ip = ip.lower()
            matched = False

            for i in p['intents']:
                if ip in i['patterns']:
                    k = random.randint(0, len(i['responses']) - 1)
                    responses.append((ip, i['responses'][k]))
                    matched = True
                    break

            # if ip == 'a' or ip == 'b' or ip == 'c' or ip == 'd':
            #     return 'Data Stored \n\n\nEnter Hi'

            if not matched:
                responses.append((ip, 'Please enter a valid input'))

        formatted_responses = ''

        for ip, res in responses:
            formatted_responses += f'{res}'

        return formatted_responses


chat_bot = ChatInterface()

#------------------------------------------


def index(request):
    return render(request, "index.html")

def index_li(request):
    return render(request, "index_li.html")    

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = CustomUser(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('physio_category')  
            else:
                messages.error(request, 'Invalid login credentials')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def email(request):
    uEmail = request.POST.get('email_address')
    uObj = saveEmail(Email = uEmail)
    uObj.save()

    return render(request, 'index.html', {'msg': 'Your Email has been recorded'})

def game_selection(request):
    # Your view logic here
    return render(request, 'game_selection.html')

def physio_category(request):
    return render(request, 'physio_category.html')

def general_well(request):
    return render(request, 'Genral_well_game.html')


def cardiac(request):
    return render(request, 'cardiac_game.html')


def fall_prevention(request):
    return render(request, 'Fall_pre_game.html')


def orthopedic(request):
    return render(request, 'ortho_game.html')


def chat(request):
    user_inp = request.GET.get('user_inp', '')
    res = chat_bot.chat(user_inp)
    return HttpResponse(res)

def dashboard(request):
    return render(request, 'dashboard.html')


# GAMES

def head_game_1(request):
    game1.run_game()
    return render(request, 'Genral_well_game.html')

def shoulder_game_1(request):
    game2.run_game()
    return render(request, 'cardiac_game.html')

def shoulder_game_2(request):
    game3.run_game()
    return render(request, 'cardiac_game.html')

def shoulder_exercise_data(request):
    if request.method == 'POST':
        # Handle form submissiongloba
        global age
        age = int(request.POST.get('age', 0))
        global shoulder_injury_history
        shoulder_injury_history = request.POST.get('shoulder_injury_history', 'no') == 'yes'
        print("Age=",age)
        print("Injury=",shoulder_injury_history)
    return render(request, 'shoulderwin.html',{'age':age,'injury':shoulder_injury_history})

def shoulder_ex(request):
    return StreamingHttpResponse(shoulder.main(age,shoulder_injury_history), content_type="multipart/x-mixed-replace;boundary=frame")
def shoulderwin(request):
    return render(request, 'shoulderwin.html')

def leg_exercise_data(request):
    if request.method == 'POST':
        # Handle form submissiongloba
        global age
        age = int(request.POST.get('age', 0))
        global leg_injury_history
        leg_injury_history = request.POST.get('leg_injury_history', 'no') == 'yes'
        print("Age=",age)
        print("Injury=",leg_injury_history)
    return render(request, 'legwin.html',{'age':age,'injury':leg_injury_history})

def leg_ex(request):
    print("Main m age",age)
    print("Injury=",leg_injury_history)
    return StreamingHttpResponse(leg.main(age,leg_injury_history), content_type="multipart/x-mixed-replace;boundary=frame")
def legwin(request):
    return render(request, 'legwin.html')
