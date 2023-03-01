from django.shortcuts import redirect, render
from django.contrib.auth. models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Auth_System import settings
from django.core.mail  import send_mail

# landing view
def home(request):
    return render(request, 'home.html')

# signup view

def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST.get('password')
        pass2 = request.POST['confirmpassword']
        
        # checking for similar username
        if User.objects.filter(username = username):
            messages.error(request, 'Username already exist! Please try another.')
            return redirect('home')
        
        # checking whether email already existed or not.
        if User.objects.filter(email=email):
            messages.error(request, 'Email already exist.')
            return redirect('home')

        # matching password and re enter password
        if  pass1 != pass2:
            messages.error(request, 'Password did not match.')
            return redirect('home')

        # checking conditions for username
        if not username.isalnum() or not username.isalpha() or not username.isnumeric():
            messages.error(request, 'username is not valid! please use both alphabhet and numbers')
            return redirect('home') 


        # creating new user
        myuser = User.objects.create_user(username=username, email =email, password =pass1)

        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()

        messages.success(request, 'Your Account has been successfully created')
        

        subject = 'Welcome to Django Login'
        msg = 'hello'+ myuser.first_name + '/n'+'Welcome' + 'Thank You for visting our website'
        from_email = settings.EMAIL_HOST_USER
        to_email= [email,]
        send_mail(subject, msg, from_email, to_email, fail_silently=True)

        return redirect('/signin')

    return render(request, 'signup.html')


# sign_in view
def signin(request):

    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username= username, password = password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'home.html', {'fname':fname})

        else:
            messages.error(request,'Worng Credentials')
            return redirect('/home')

    return render(request, 'signin.html')


def signout(request):
    print("--------------------------------")
    logout(request)
    messages.success(request,'You Logged Out successfully')
    return redirect('home')
