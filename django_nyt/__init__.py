# -*- coding: utf-8 -*-
_disable_notifications = False

VERSION = "0.9"

def notify(message, key, target_object=None, url=None, filter_exclude={}):
    """
    Notify subscribing users of a new event. Key can be any kind of string,
    just make sure to reuse it where applicable! Object_id is some identifier
    of an object, for instance if a user subscribes to a specific comment thread,
    you could write:
    
    notify("there was a response to your comment", "comment_response", 
           target_object=PostersObject, 
           url=reverse('comments:view', args=(PostersObject.id,)))
    
    The below example notifies everyone subscribing to the "new_comments" key
    with the message "New comment posted".
    
    notify("New comment posted", "new_comments")
    
    filter_exclude: a dictionary to exclude special elements of subscriptions
    in the queryset, for instance filter_exclude={''}
    
    """

    # TODO: Can we improve this? In __init__.py we don't want it in the main scope
    # because then we have to be in a django project to do "import django_nyt", but
    # for instance then we cannot do "from django_nyt import VERSION" in setup.py
    from django.contrib.contenttypes.models import ContentType
    from django.db.models import Model
    from django.utils.translation import ugettext as _

    from . import models

    if _disable_notifications:
        return 0
    
    if target_object:
        if not isinstance(target_object, Model):
            raise TypeError(_(u"You supplied a target_object that's not an instance of a django Model."))
        object_id = target_object.id
    else:
        object_id = None
        
    objects = models.Notification.create_notifications(
        key, 
        object_id=object_id, 
        message=message, 
        url=url, 
        filter_exclude=filter_exclude,
    )
    return len(objects)
    