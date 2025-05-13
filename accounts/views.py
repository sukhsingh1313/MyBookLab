from django.shortcuts import redirect,render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from BookLab_App.forms import SingupForm,LoginForm
from django.contrib import messages
from django.core.mail import send_mail
from .models import EmailDevice
from django.template.loader import render_to_string
import random
import string


def generate_otp(length=6):
   return ''.join(random.choices(string.digits, k=length))

def signup_view(request):
    if request.method == 'POST':
        form  = SingupForm(request.POST)
        if form.is_valid():
            user   = form.save(commit=False)
            user.is_active = False
            user.save()

            #generate and save otp
            otp = generate_otp()
            EmailDevice.objects.filter(user =user).delete() # remove any exesting OTP device
            email_device = EmailDevice(user =user,otp =otp,email = form.cleaned_data['email'])
            email_device.save()

            #render otp template
            html_message= render_to_string('otp_email.html',{'username':user.username,'otp':otp})
            #send otp email
            send_mail(
                'Your OTP Verification Code',
                f'Your OTP is {otp}',
                'your-email@example.com',
                [form.cleaned_data['email']],
                
                html_message= html_message
            )
            return redirect('otp_verification', user_id=user.id)
    else:
        form = SingupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def otp_verification(request, user_id):
    if request.method == 'POST':
        otp =  request.POST.get('otp')
        email_device = EmailDevice.objects.get(user_id =user_id)
        if email_device.verify_otp(otp):
            user = email_device.user
            user.is_active = True
            user.save()
            login(request,user)
            return redirect('main_book_section')
    return render(request,'otp_verification.html',{'user_id': user_id})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect('main_book_section')
            else:
                form.add_error(None,"Invalid username or password")
    else:
        form =  LoginForm()
    return render(request,'accounts/login.html',{'form':form})

@login_required
def logout_view(request):
     logout(request)
     messages.success(request, 'You have successfully logged out') 
     return redirect('login_view')
