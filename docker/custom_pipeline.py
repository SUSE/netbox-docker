from netbox.authentication import Group
from os import getenv

NETBOX_ADMIN_GROUP = getenv('NB_PIPELINE_NB_ADMIN_GROUP', 'admins')
SUSEID_ADMIN_GROUP = getenv('NB_PIPELINE_IDP_ADMIN_GROUP', 'app-netbox-admins')
DEFAULT_GROUP = getenv('NB_PIPELINE_NB_DEFAULT_GROUP', 'default-users')

class AuthFailed(Exception):
    pass

def update_groups(response, user, backend, *args, **kwargs):

    if 'groups' not in response:
        user.groups.clear()
        user.save()
        return

    groups = response['groups']

    updated_user = False

    # Remove unmanaged groups
    for group in user.groups.all():
        if group.name != DEFAULT_GROUP and group.name != NETBOX_ADMIN_GROUP:
            user.groups.remove(group)
            updated_user = True

    user_groups = [item.name for item in user.groups.all()]

    # User is not in netbox admin group but should be. Update memberships.
    if SUSEID_ADMIN_GROUP in groups and NETBOX_ADMIN_GROUP not in user_groups:
        group, created = Group.objects.get_or_create(name=NETBOX_ADMIN_GROUP)
        user.groups.add(group)
        updated_user = True

    # User is in netbox admin group but should not be. Update memberships.
    if SUSEID_ADMIN_GROUP not in groups and NETBOX_ADMIN_GROUP in user_groups:
        group = Group.objects.get(name=NETBOX_ADMIN_GROUP)
        user.groups.remove(group)
        updated_user = True

    # Add default group if not already done.
    if DEFAULT_GROUP not in user_groups:
        group, created = Group.objects.get_or_create(name=DEFAULT_GROUP)
        user.groups.add(group)
        updated_user = True

    if updated_user:
        user.save()
