from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
from django.urls import reverse
from django.views import View
from .models import *

from django.core.mail import send_mail, EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from  django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import *
from django.contrib.sites.shortcuts import get_current_site


def send_email_otp(x,user_email,otp):


    subject = 'Verification Code'
    print('line no 41',x.first_name,x.last_name,otp)

    html_content = render_to_string('otp_email_template.html',
                                    {'first_name': x.first_name, 'last_name': x.last_name,'otp':otp
                                     })
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, 'adnanrafique340@gmail.com', user_email)
    msg.attach_alternative(html_content, "text/html")

    msg.send()

    return None

def Login(request):


    if request.method == 'POST':
        Username = request.POST.get('username')
        Password = request.POST.get('password')
        if not Username:
            messages.error(request, 'Email is required')
            return redirect('Login')
        if not Password:
            messages.error(request, 'Password is required')
            return redirect('Login')
        x=User.objects.filter(username=Username).first()

        user_profile = Profile.objects.filter(owner=x).first()

        if x is None:
            messages.error(request,'No User found with this Email')
            return render(request, 'Login.html')

        if x.is_active:
            user = auth.authenticate(username=Username, password=Password)
            if user is not None:

                otp = str(random.randint(1000, 9999))
                print(otp)
                user_profile.otp = otp
                user_profile.save()


                user_email = []
                user_email.append(x.email)
                print('line no 84 receiver email list', user_email)
                send_email_otp(x, user_email, otp)

                print('OTP is:', otp)


                request.session['Username'] = Username
                request.session['Password'] = Password
                return redirect('login_otp')
            else:
                messages.error(request, 'Invalid Email or Password')
                redirect('Login')
        else:
            messages.error(request, 'Account is not activated, Please check your Email')
            redirect('Login')



    return render(request, 'Login.html')


def login_otp(request):

    Username = request.session['Username']
    Password = request.session['Password']


    if request.method == 'POST':
        digit_1 = request.POST.get('digit_1')
        digit_2 = request.POST.get('digit_2')
        digit_3 = request.POST.get('digit_3')
        digit_4 = request.POST.get('digit_4')
        otp = digit_1 + digit_2 + digit_3 + digit_4
        if not otp:
            messages.error(request, 'OTP required')
            return redirect('login_otp')
        profile = Profile.objects.filter(owner__username=Username).first()
        print('Line no 107',profile.otp)

        if otp == profile.otp:

            user = auth.authenticate(username=Username, password=Password)
            print('Line no 112',user)
            if user is not None:
                if user.is_active:
                 login(request, user)


                 return redirect('dashboard')

                else:
                    messages.error(request,'Account is not activated')
            else:
             messages.warning(request, 'Invalid ID or password')
             return redirect('Login')

        else:
            messages.error(request,'Invalid OTP,please try again')
            return render(request, 'Login_otp.html')

    return render(request, 'Login_otp.html')


def Sign_Up(request):

    if request.method == 'POST':

        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        Email = request.POST.get('Email')


        country_code = request.POST.get('country_code')

        char1 = '('
        char2 = ')'
        mystr = country_code

        perfect_country_code = mystr[mystr.find(char1) + 1: mystr.find(char2)]

        print(perfect_country_code)
        Phone_no_input = request.POST.get('phone_no')

        print('phone no final rep is=', perfect_country_code + Phone_no_input)
        Phone_no = perfect_country_code + Phone_no_input


        Password = request.POST.get('Password')


        username = Email
        if not f_name:
            messages.error(request, 'First Name is required')
            return redirect('Sign_up')
        if not l_name:
            messages.error(request, 'Last Name is required')
            return redirect('Sign_up')
        if not Email:
            messages.error(request, 'Email is required')
            return redirect('Sign_up')
        if not Phone_no:
            messages.error(request, 'Phone is required')
            return redirect('Sign_up')
        if not Password:
            messages.error(request, 'Password is required')
            return redirect('Sign_up')



        try:
            if not User.objects.filter(username=username).exists():

                if not Profile.objects.filter(phone=Phone_no):

                    x = User.objects.create_user(first_name=f_name, last_name=l_name, email=Email,
                                                 username=username, password=Password)
                    x.is_active = False

                    y = Profile.objects.create(owner=x, phone=Phone_no)

                    x.save()
                    y.save()

                    uidb64 = urlsafe_base64_encode(force_bytes(x.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(x)})
                    activate_url = 'http://' + domain + link

                    print('activate url is:', activate_url)

                    user_email = []
                    user_email.append(Email)

                    subject = 'Thank you for account creation with us.'

                    html_content = render_to_string('email_template.html',
                                                    {'first_name': x.first_name, 'last_name': x.last_name,
                                                     'activate_url': activate_url,

                                                     })
                    text_content = strip_tags(html_content)

                    msg = EmailMultiAlternatives(subject, text_content, 'adnanrafique340@gmail.com', user_email)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    messages.info(request, 'Account Created Successfully. Please check your email to activate account.')
                    return redirect('Login')





                else:
                    messages.info(request, 'User is already exist against this Phone No ')
                    return redirect('Sign_up')




            messages.info(request, 'User is already exist against this Email.')
            return redirect('Sign_up')
        except Exception as e:
            messages.info(request, 'Ops something happens unwanted.')
            return redirect('Sign_up')
    else:
        return render(request, 'Sign_Up.html')



def forget_password(request):
    if request.method == 'POST':
        Username = request.POST.get('un')
        if not Username:
            messages.error(request, 'Email is required')
            return redirect('forget_password')

        user=User.objects.filter(username=Username).first()
        print(user)

        x= Profile.objects.filter(owner=user).first()
        if user is None:
            messages.error(request,'User not found with this Email')
            return render(request, 'forget-password.html')

        otp = str(random.randint(1000, 9999))
        x.otp = otp
        x.save()

        user_email = []
        user_email.append(user.email)
        send_email_otp(user, user_email, otp)


        request.session['Username'] = Username

        return redirect('reset_password')

    return render(request,'forget-password.html')


def reset_password(request):

    Username = request.session['Username']


    if request.method == 'POST':
        digit_1 = request.POST.get('digit_1')
        digit_2 = request.POST.get('digit_2')
        digit_3 = request.POST.get('digit_3')
        digit_4 = request.POST.get('digit_4')
        otp = digit_1 + digit_2 + digit_3 + digit_4
        profile = Profile.objects.filter(owner__username=Username).first()

        print('Line no 278',profile.otp)

        if otp == profile.otp:

             request.session['Username'] = Username
             messages.success(request, 'Verification code match successfully')
             return redirect('update_password')

        else:
            messages.error(request,'Invalid OTP')
            return render(request, 'reset_password_otp.html')

    return render(request, 'reset_password_otp.html')


def update_password(request):
    Username = request.session['Username']


    if request.method == 'POST':
        users = User.objects.get(username=Username)

        new_password = request.POST.get('new_password')



        if len(new_password)!=0:
            users.set_password(new_password)
            users.save()

            messages.info(request, 'Password updated successfully,Please Login with New Set Password')
            return redirect('Login')

    else:

     return render(request,'update_password.html')




def Logout(request):
    logout(request)
    messages.info(request,'You have been Logged Out')
    return redirect('Login')

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)

            print('Line no 336',user.username)

            if user.is_active:
                messages.info(request,'Your account is already activated\nUse your credentials to Login')
                return redirect('Login')
            else:
                user.is_active=True
                user.save()
                messages.success(request,'Account Activated Successfully')
                return redirect('Login')

        except Exception as e:
            print('Line no 208 Exception is',e)
            pass
        return redirect('Login')