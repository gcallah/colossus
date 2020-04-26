from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from colossus.apps.notifications.constants import Actions
from colossus.apps.notifications.models import Notification


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class NotificationListView(ListView):
    """
    A class to display all the notifications in list view.
    """
    model = Notification
    context_object_name = 'notifications'
    paginate_by = 100
    ordering = '-date'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.request.user.notifications.filter(is_seen=False).update(is_seen=True)
        return response


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class NotificationDetailView(DetailView):
    """
    A class to display the notification in detailed view.
    """
    model = Notification
    context_object_name = 'notification'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object.is_read:
            self.object.is_read = True
            self.object.save(update_fields=['is_read'])
        return response


@login_required
@csrf_exempt
def unread(request):
    """
    A function to mark the notification as seen after the user has seen it.
    """
    notifications = Notification.objects.filter(user=request.user).order_by('-date')
    notifications.update(is_seen=True)
    context = {
        'notifications': notifications[:5],
        'Actions': Actions
    }
    html = render_to_string('notifications/_unread.html', context, request)
    return JsonResponse({'html': html})


@login_required
@require_POST
@csrf_exempt
def mark_all_as_read(request):
    """
    A function to mark the notification as read after the user reads it.
    """
    request.user.notifications.update(is_read=True, is_seen=True)

    # If the request is ajax, it means it came from the small notifications widget on the top menu
    if request.is_ajax():
        return unread(request)

    return redirect('notifications:notifications')


@login_required
@require_POST
@csrf_exempt
def clear_all(request):
    """
    A function to delete all the notifications.
    """
    request.user.notifications.all().delete()

    # If the request is ajax, it means it came from the small notifications widget on the top menu
    if request.is_ajax():
        return unread(request)

    return redirect('notifications:notifications')
