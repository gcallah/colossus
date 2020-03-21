def notifications(request):
    """
    A function to get the total count of all the notifications.

    Keyword Arguments:
    request -- A Http request object

    Returns:
    dict -- A dictionary mentioning the total count of notifications.
    If no notifications are there, it returns an Empty Dictionary.
    """
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_seen=False).count()
        return {
            'notifications_count': count
        }
    else:
        return dict()
