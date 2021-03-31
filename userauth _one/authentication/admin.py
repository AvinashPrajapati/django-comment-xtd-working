from django.contrib import admin

from . import models

def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request,)

send_newsletter.short_description = "Send selected Newsletters to all subscribers"

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

admin.site.register(models.Post, PostAdmin)

admin.site.register(models.Subscriber)

class NewsletterAdmin(admin.ModelAdmin):
    actions = [send_newsletter]

admin.site.register(models.Newsletter, NewsletterAdmin)


# Register your models here.
