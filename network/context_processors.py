def unread_notifications(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications': request.user.notifications.filter(read=False).count()
        }
    return {'unread_notifications': 0}

def is_moderator(request):
    if request.user.is_authenticated:
        return {
            'is_moderator': request.user.groups.filter(name='Moderator').exists()
        }
    return {'is_moderator': False}
