from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.middleware.csrf import get_token


from .models import patient_details,notes
import random
import string

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string is:", result_str)


def patientProfile(request):
    return render(request, 'patient/patient_profile.html')
def patientRecords(request):
    return render(request, 'patient/patient_records.html')


def personalNotes(request):
    csrf_token = get_token(request)
    csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" />'.format(csrf_token)
    if request.user.is_authenticated:
        user=request.user
        if len(notes.objects.filter(username_p=user.username))==0:
            new_note=notes()
            new_note.username_p=user.username
            new_note.description='Add your notes here'
            new_note.save()

        note=notes.objects.get(username_p=user.username)
        return render(request, 'patient/personalNotes.html',{"des":note.description})
        

def labreports(request):
    return render(request, 'patient/labreports.html')
def medications(request):
    return render(request, 'patient/medications.html')

def registerpage(request):
    return render(request,'patient/register.html')

def signup(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
       
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
       

        if len(username)>15:
            messages.error(request,'length of username should be less than15')
            return redirect('patient:registerpage')
        
        myuser=User.objects.create_user(username,email,password)
        myuser.first_name=fname
        myuser.last_name=lname
       
       
        myuser.save()
       
        print("1")

        patient=patient_details()
        patient.fname=fname
        patient.lname=lname
        patient.username=username
        patient.auth_key=get_random_string(8)
        patient.email=email
        patient.save()
        
        print('2')
        messages.success(request, 'Form submission successful')
        return redirect('/')
       

    else :
        return HttpResponse('404-not found')




def loginn(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            print("innn")
            request.session["username_p"]=username
            return render(request,'patient/patient_profile.html')

        else :
            print("invalid credentials")
            return render(request,'centralapp/mainpage.html')


        return HttpResponse('login')



    else:
        return HttpResponse('404-not found')

def logout(request):
    if request.method=="POST":
        logout(request)
        return render(request,'patient/mainpage.html') 
    return HttpResponse('logout')


def addnotes(request):
    if request.user.is_authenticated:
        user=request.user
        description=request.POST['description']
        username= user.username
        if len(notes.objects.filter(username_p=username))!=0:
            notes.objects.filter(username_p=username).delete()
            new_note=notes()
            new_note.username_p=username
            new_note.description=description
            new_note.save()
        else:
            new_note=notes()
            new_note.username_p=username
            new_note.description=description
            new_note.save()


        return redirect('patient:personalNotes')
        
       


    

