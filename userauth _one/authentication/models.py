from django.db import models
from django.urls import reverse
from django.core.mail import send_mass_mail
from django.conf import settings
from django_comments_xtd.moderation import moderator, SpamModerator
from authentication.badwords import badwords

# Create your models here.
class Post (models.Model):
    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    content = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('authentication:postDetail', args=[self.slug])



class PostCommentModerator(SpamModerator):
    email_notification = True
    # removal_suggestion_notification = True

    def moderate(self, comment, content_object, request):
        # Make a dictionary where the keys are the words of the message
        # and the values are their relative position in the message.
        def clean(word):
            ret = word
            if word.startswith('.') or word.startswith(','):
                ret = word[1:]
            if word.endswith('.') or word.endswith(','):
                ret = word[:-1]
            return ret

        lowcase_comment = comment.comment.lower()
        msg = dict([(clean(w), i)
                    for i, w in enumerate(lowcase_comment.split())])
        for badword in badwords:
            if isinstance(badword, str):
                if lowcase_comment.find(badword) > -1:
                    return True
            else:
                lastindex = -1
                for subword in badword:
                    if subword in msg:
                        if lastindex > -1:
                            if msg[subword] == (lastindex + 1):
                                lastindex = msg[subword]
                        else:
                            lastindex = msg[subword]
                    else:
                        break
                if msg.get(badword[-1]) and msg[badword[-1]] == lastindex:
                    return True
        return super(PostCommentModerator, self).moderate(comment,
                                                          content_object,
                                                          request)

moderator.register(Post, PostCommentModerator)

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"

class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.TextField()

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")


    def send(self, request):
        subscribers = Subscriber.objects.filter(confirmed=True)
        for sub in subscribers:
            message1 = (self.subject,self.contents+f'http://127.0.0.1:8000/unsuscribe/{sub.conf_num}', settings.EMAIL_HOST_USER,[sub.email],)
            send_mass_mail((message1,), fail_silently=False)
    