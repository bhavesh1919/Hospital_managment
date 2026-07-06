from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect

from pro1 import settings
from .models import Register

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from pro1 import info
from django.core.mail import send_mail


# Create your views here.
def index(req ):
    return render(req,'index.html')

def Login(req):

    if req.method=="POST":
        username=req.POST["Username"]
        password=req.POST["Password"]

        user = authenticate(username=username,password=password)

        if user is not None:
            login(req,user)
            return redirect('/')
        
        else:
            messages.error(req,"Bed credentail")
            return redirect("/login/")
        
    return render(req,'login.html')


def logout(req):    
    logout(messages)
    messages.success(req,"you are successful logout")
    return redirect("/")
    
def Registr(req):
    if req.method=='POST':
        username=req.POST.get('Name')
        fname=req.POST.get('fName')
        lname=req.POST.get('lName')
        #phone=req.POST.get('Phone')
        email=req.POST.get('Email')
        password=req.POST.get('Password')


        if User.objects.filter(username=username):
            messages.error(req," user will be alredy exists")
            return redirect("/login")

        myuser = User.objects.create_user(username,email,password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()

        messages.success(req,"registration will be successfully")


       #welcom email

        subject="welcome to Hospital Managment system"
        message="Hello"+myuser.first_name+myuser.last_name+"\n"+"welcome\n "+"your are succesfully Regiter in our system"
        from_email=info.EMAIL_HOST_USER
        to_list=[myuser.email]
        print(myuser.email)
        send_mail(subject,message,from_email,to_list,fail_silently=False)

        # register = Register.objects.create(name=name,phone=phone,email=email,password=password)

        return redirect('/login/')
    return render(req,'Register.html')


def patient_dashboard(req):
    return render(req,"patient_dashboard.html")

def docter_Registr(req):
    return render(req,'doctor_registration.html')

def about_us(req):
    return render(req,'about-us.html')

def contact(req):
    return render(req,'contact.html')

def admin_dash(req):
    return render(req,'admin_dash.html')