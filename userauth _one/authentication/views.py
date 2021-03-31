from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Subscriber
from django.contrib import messages
import uuid
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def home(request):
    postList = Post.objects.all()
    # print(postList)
    context = {
        'postList': postList,
    }
    return render(request, 'home.html', context)


def postDetail(request, slug):
    postdetail = get_object_or_404(Post, slug=slug)
    context = {
        'postdetail': postdetail,
    }
    return render(request, 'postdetail.html', context)


def userProfile(request):
    context = {

    }
    return render(request, 'userprofile.html', context)


def newsletter_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            suscribe_obj =Subscriber.objects.filter(email=email, confirmed=False).first()
            if suscribe_obj:
                suscribe_obj.confirmed = True
                suscribe_obj.save()
                messages.success(request, 'Thank you to be here again !')
                return redirect('authentication:home')

            if Subscriber.objects.filter(email=email, confirmed=True).first():
                messages.warning(request, 'This email has been already suscribed!!!')
                return redirect('authentication:home')

            token = str(uuid.uuid4())
            suscriber = Subscriber(email=email, conf_num=token)
            suscriber.save()
            send_mail_suscription(email, token)
            messages.success(
                request, 'Check your email to confirm that it is you.')
            return redirect('authentication:home')

        except Exception as e:
            messages.error(request, 'Something went wrong.')
            return redirect('authentication:home')

def verify(request, token):
    try:
        suscribe_obj = Subscriber.objects.filter(conf_num=token).first()
        if suscribe_obj:
            suscribe_obj.confirmed = True
            suscribe_obj.save()
            messages.success(request, 'Thanks ! Your suscription has been added successfully.')
            return redirect('authentication:home')
    except Exception as e:
        messages.error(request, 'Something went wrong')
        return redirect('authentication:home')

def delete_suscription(request, token):
    try:
        suscribe_obj = Subscriber.objects.filter(conf_num=token).first()
        if suscribe_obj:
            suscribe_obj.confirmed = False
            suscribe_obj.save()
            messages.success(request, 'Sorry to see you to go.')
            return redirect('authentication:home')
        else:
            messages.success(request, 'You have not suscribed or your suscription has been removed')
            return redirect('authentication:home')
    except Exception as e:
        messages.error(request, 'Something went wrong')
        return redirect('authentication:home')



def send_mail_suscription(email, token):
    subject = 'Your email need to be verify'
    message = 'Nice to be with you.'
    html_message = f"<br><strong>Dear,</strong><p>Sir, Mam</p><br> <p>You or someone with your email has suscribe to our newsletter. <br>I hope that it will be you, if not then just ignore this email else, <br>  click the link given below to verify your self that it's you.</p> <strong><a href='http://127.0.0.1:8000/verify/{token}'>Click here to verify</a></strong> <br><br> <p>Thanks, your regard.</p>"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email,
              recipient_list, html_message=html_message)
