from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from colossus.apps.campaigns.models import Campaign
from colossus.apps.lists.models import MailingList


def render_import_completed(notification):
    """
    A function to render a message if importing subscribers is completed successfully.

    Functional arguments:
    notification -- An object of Notification model class.
    """
    data = notification.data
    mailing_list = MailingList.objects.values('id', 'name').get(pk=data['mailing_list_id'])
    data['mailing_list_name'] = escape(mailing_list['name'])
    message = _('<strong>Import completed with success!</strong> %(created)s created, %(updated)s updated, and '
                '%(ignored)s ignored to list %(mailing_list_name)s.') % data
    return mark_safe(message)


def render_import_errored(notification):
    """
    A function to render a message if there is an error in importing subscribers.

    Functional arguments:
    notification -- An object of Notification model class.
    """
    data = notification.data
    mailing_list = MailingList.objects.values('id', 'name').get(pk=data['mailing_list_id'])
    data['mailing_list_name'] = escape(mailing_list['name'])
    message = _('<strong>Import failed.</strong> An error occurred while trying to import subscribers to '
                'list %(mailing_list_name)s.') % data
    return mark_safe(message)


def render_campaign_sent(notification):
    """
    A function to render the mailing list name of a campaign, if sent successfully.

    Functional arguments:
    notification -- An object of Notification model class.
    """
    data = notification.data
    campaign = Campaign.objects.select_related('mailing_list').get(pk=data['campaign_id'])
    data['campaign_name'] = escape(campaign.name)
    data['recipients_count'] = campaign.recipients_count
    data['mailing_list_name'] = escape(campaign.mailing_list.name)
    message = _('<strong>Campaign "%(campaign_name)s" was sent</strong> to %(recipients_count)s subscribers '
                'from list %(mailing_list_name)s.') % data
    return mark_safe(message)


def render_list_cleaned(notification):
    """
    A function to render a message if the mailing list is cleaned.

    Functional arguments:
    notification -- An object of Notification model class.
    """
    data = notification.data
    mailing_list = MailingList.objects.values('id', 'name').get(pk=data['mailing_list_id'])
    data['mailing_list_name'] = escape(mailing_list['name'])
    message = _('<strong>Cleaned</strong> %(cleaned)s emails from list %(mailing_list_name)s.') % data
    return mark_safe(message)
