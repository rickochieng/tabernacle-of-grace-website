import json
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import *


def page(template):
    @ensure_csrf_cookie
    def view(request):
        sermons = Sermon.objects.filter(published=True)
        events = Event.objects.filter(published=True, date__gte=timezone.localdate())
        if template == 'index.html':
            sermons, events = sermons[:3], events[:5]
        return render(request, template, {'sermons': sermons, 'events': events, 'photos': Photo.objects.all()})
    return view


@require_POST
def submit(request, kind):
    try:
        f = [str(x).strip()[:2000] for x in json.loads(request.body)['fields']]
        subject = body = None
        if kind == 'subscribe':
            validate_email(f[0])
            Subscriber.objects.get_or_create(email=f[0].lower())
        elif kind == 'prayer' and f[3]:
            PrayerRequest.objects.create(name=f[0] or 'Anonymous', contact=f[1], category=f[2], request=f[3])
            subject, body = f'New prayer request ({f[2]})', f'From: {f[0] or "Anonymous"} ({f[1]})\n\n{f[3]}'
        elif kind == 'contact' and f[3]:
            ContactMessage.objects.create(name=f[0] or 'Anonymous', contact=f[1], subject=f[2], message=f[3])
            subject, body = f'New message: {f[2] or "(no subject)"}', f'From: {f[0]} ({f[1]})\n\n{f[3]}'
        else:
            raise ValueError
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Please fill in the form correctly and try again.'}, status=400)
    to = SiteDetails.load().notification_email
    if subject and to:
        send_mail(subject, body, None, [to], fail_silently=True)
    return JsonResponse({'ok': True})
