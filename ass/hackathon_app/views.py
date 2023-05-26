from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Hackathon, Registration, User, Submissions
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['POST'])
def login_api(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
@api_view(['GET'])
def all_hackathon_lists(request):
    if request.method == 'GET':
        hackathons = Hackathon.objects.all()
        hackathon_data = []
        for hackathon in hackathons:
            hackathon_data.append({
                
                'id': hackathon.id,
                'title': hackathon.title,
                'description': hackathon.description,
                'author':{
                    'id': hackathon.user.id,
                    'username': hackathon.user.username,
                },
                'background_image': hackathon.background_image.url if hackathon.background_image else None,
                'hackathon_image': hackathon.hackathon_image.url if hackathon.hackathon_image else None,
                'start_time': hackathon.start_time,
                'end_time': hackathon.end_time,
                'reward': hackathon.reward,
                })
            
        return JsonResponse({'hackathons': hackathon_data}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

@csrf_exempt
@login_required
@api_view(['POST'])
def create_hackathon(request):
    user_id = request.user.id
    if request.method == 'POST':
        if request.user.is_superuser:
            user = User.objects.get(id=user_id)
            title = request.POST.get('title')
            description = request.POST.get('description')
            background_image = request.FILES.get('background_image')
            hackathon_image = request.FILES.get('hackathon_image')
            type_submission = request.POST.get('type_submission')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('End_time')
            reward = request.POST.get('reward')
            exists = Hackathon.objects.filter(user = user, title = title, description = description, background_image = background_image, hackathon_image = hackathon_image, type_submission = type_submission, start_time = start_time, end_time = end_time, reward = reward).exists()
            
            if exists:
                return JsonResponse({'error': "HAckathon already Exists"})
            
            hackathon = Hackathon.objects.create(user = user, title = title, description = description, background_image = background_image, hackathon_image = hackathon_image, type_submission = type_submission, start_time = start_time, end_time = end_time, reward = reward)
            return JsonResponse({
                'id': hackathon.id,
                'title': hackathon.title,
                'description': hackathon.description,
                'author':{
                    'id': hackathon.user.id,
                    'username': hackathon.user.username,
                },
                'background_image': hackathon.background_image.url if hackathon.background_image else None,
                'hackathon_image': hackathon.hackathon_image.url if hackathon.hackathon_image else None,
                'start_time': hackathon.start_time,
                'end_time': hackathon.end_time,
                'reward': hackathon.reward,
                }, status=201)
        else:
            return JsonResponse({'error' : 'Only an Admin can create a new Hackathon'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
@login_required
@api_view(['POST'])
def register(request, hackathon_id):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        hackathon = Hackathon.objects.get(id=hackathon_id)
        status = request.POST.get('status')
        if status == False:
            return JsonResponse({'error': 'Use unregister api for """status == false"""'})
        exists = Registration.objects.filter(user = user, hackathon=hackathon).exists()
        if exists:
            return JsonResponse({'error' : 'You are already registered'}, status=400)
        register_object = Registration.object.create(user=user, hackathon=hackathon, status=status)
        return JsonResponse({
                'current_status': "Succesfully Registered",
                'id': hackathon.id,
                'title': hackathon.title,
                'description': hackathon.description,
                'author':{
                    'id': hackathon.user.id,
                    'username': hackathon.user.username,
                },
                'background_image': hackathon.background_image.url if hackathon.background_image else None,
                'hackathon_image': hackathon.hackathon_image.url if hackathon.hackathon_image else None,
                'start_time': hackathon.start_time,
                'end_time': hackathon.end_time,
                'reward': hackathon.reward,
                }, status=201)
        
        
@csrf_exempt
@login_required
@api_view(['PATCH'])
def unregister(request, hackathon_id):
    if request.method == 'PATCH':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        hackathon = Hackathon.objects.get(id=hackathon_id)
        exists = Registration.objects.filter(user = user, hackathon=hackathon).exists()
        if exists == False:
            return JsonResponse({'error' : 'You have not registered to this Hackathon'}, status=400)
        status = request.POST.get('status')
        if status == False:
            return JsonResponse({'error': 'You already unregistered for this hackathon'})
        record = Registration.objects.get(user=user, hackathon=hackathon)
        record.status = True
        record.save()
        return JsonResponse({
                'current_status': "Succesfully Unregistered",
                }, status=201)
        
        
@csrf_exempt
@login_required
@api_view(['GET'])
def view_all_registrations_currentUser(request):
    if request.method == 'GET':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        registrations = Registration.objects.all(user=user)
        hackathon_data = []
        for registration in registrations:
            hackathon = registration.hackathon
            hackathon_data.append({
                
                'id': hackathon.id,
                'title': hackathon.title,
                'description': hackathon.description,
                'author':{
                    'id': hackathon.user.id,
                    'username': hackathon.user.username,
                },
                'background_image': hackathon.background_image.url if hackathon.background_image else None,
                'hackathon_image': hackathon.hackathon_image.url if hackathon.hackathon_image else None,
                'start_time': hackathon.start_time,
                'end_time': hackathon.end_time,
                'reward': hackathon.reward,
                })
        return JsonResponse({'hackathons': hackathon_data}, status=200)
    
    else:
        JsonResponse({'error':'Bad Request'}, status=400)


@csrf_exempt
@login_required
@api_view(['GET'])
def view_all_registrations_anyUser(request):
    if request.method == 'GET' and request.user.is_superuser:
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        registrations = Registration.objects.all(user=user)
        hackathon_data = []
        for registration in registrations:
            hackathon = registration.hackathon
            hackathon_data.append({
                
                'id': hackathon.id,
                'title': hackathon.title,
                'description': hackathon.description,
                'author':{
                    'id': hackathon.user.id,
                    'username': hackathon.user.username,
                },
                'background_image': hackathon.background_image.url if hackathon.background_image else None,
                'hackathon_image': hackathon.hackathon_image.url if hackathon.hackathon_image else None,
                'start_time': hackathon.start_time,
                'end_time': hackathon.end_time,
                'reward': hackathon.reward,
                })
        return JsonResponse({'hackathons': hackathon_data}, status=200)
    
    else:
        JsonResponse({'error':'Bad Request'}, status=400)


@csrf_exempt
def submission_type(request):
    choices = ['Image', 'Text', 'Link']
    return JsonResponse({'choices' : choices}, status=200)


@csrf_exempt
@login_required
@api_view(['POST'])
def create_submission(request):
    if request.method == 'POST':
        user_id = request.user.id
        hackathon_id = request.POST.get('hackathon_id')
        user = User.objects.get(id=user_id)
        hackathon = Hackathon.objects.get(id=hackathon_id)
        name = request.POST.get('name')
        summary = request.POST.get('summary')
        sub_type = request.POST.get('sub_type')
        if sub_type == 'TEXT':
            text_submission = request.POST.get('text_submission')
            Submissions.objects.create(user=user, hackathon=hackathon, name=name, summary=summary, text_submission=text_submission)
        elif sub_type == 'LINK':
            link_submission = request.POST.get('link_submission')
            Submissions.objects.create(user=user, hackathon=hackathon, name=name, summary=summary, link_submission=link_submission)
        else:
            image_submission = request.FILE.get('image_submission')
            Submissions.objects.create(user=user, hackathon=hackathon, name=name, summary=summary, image_submission=image_submission)
        
        return JsonResponse({'message': "successfully submitted"}, status=200)


            


        
        
