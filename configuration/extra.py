####
## This file contains extra configuration options that can't be configured
## directly through environment variables.
####

## Specify one or more name and email address tuples representing NetBox administrators. These people will be notified of
## application errors (assuming correct email settings are provided).
# ADMINS = [
#     # ['John Doe', 'jdoe@example.com'],
# ]


## URL schemes that are allowed within links in NetBox
# ALLOWED_URL_SCHEMES = (
#     'file', 'ftp', 'ftps', 'http', 'https', 'irc', 'mailto', 'sftp', 'ssh', 'tel', 'telnet', 'tftp', 'vnc', 'xmpp',
# )

## Enable installed plugins. Add the name of each plugin to the list.
# from netbox.configuration.configuration import PLUGINS
# PLUGINS.append('my_plugin')

## Plugins configuration settings. These settings are used by various plugins that the user may have installed.
## Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
# from netbox.configuration.configuration import PLUGINS_CONFIG
# PLUGINS_CONFIG['my_plugin'] = {
#   'foo': 'bar',
#   'buzz': 'bazz'
# }


## Remote authentication support
# REMOTE_AUTH_DEFAULT_PERMISSIONS = {}


## By default uploaded media is stored on the local filesystem. Using Django-storages is also supported. Provide the
## class path of the storage driver and any configuration options in STORAGES. For example:
# STORAGES = {
#     'default': {
#         'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
#         'OPTIONS': {
#             'access_key': 'Key ID',
#             'secret_key': 'Secret',
#             'bucket_name': 'netbox',
#             'region_name': 'us-west-1',
#         }
#     },
#     'staticfiles': {
#         'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
#     }
# }


## This file can contain arbitrary Python code, e.g.:
# from datetime import datetime
# now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
# BANNER_TOP = f'<marquee width="200px">This instance started on {now}.</marquee>'

from os import getenv

DEFAULT_DASHBOARD = [
    {
        'widget': 'extras.BookmarksWidget',
        'width': 4,
        'height': 5,
        'title': 'Bookmarks',
        'color': 'orange',
    },
    {
        'widget': 'extras.ObjectCountsWidget',
        'width': 4,
        'height': 2,
        'title': 'Organization',
        'config': {
            'models': [
                'dcim.site',
                'tenancy.tenant',
                'tenancy.contact',
            ]
        }
    },
    {
        'widget': 'extras.NoteWidget',
        'width': 4,
        'height': 2,
        'title': 'Welcome!',
        'color': 'green',
        'config': {
            'content': (
                'This is your personal dashboard. Feel free to customize it by rearranging, resizing, or removing '
                'widgets. You can also add new widgets using the "add widget" button below. Any changes affect only '
                '_your_ dashboard, so feel free to experiment!'
            )
        }
    },
    {
        'widget': 'extras.ObjectCountsWidget',
        'width': 4,
        'height': 3,
        'title': 'IPAM',
        'config': {
            'models': [
                'ipam.vrf',
                'ipam.aggregate',
                'ipam.prefix',
                'ipam.iprange',
                'ipam.ipaddress',
                'ipam.vlan',
            ]
        }
    },
    {
        'widget': 'extras.ObjectCountsWidget',
        'width': 4,
        'height': 3,
        'title': 'Circuits',
        'config': {
            'models': [
                'circuits.provider',
                'circuits.circuit',
                'circuits.providernetwork',
                'circuits.provideraccount',
            ]
        }
    },
    {
        'widget': 'extras.ObjectCountsWidget',
        'width': 4,
        'height': 3,
        'title': 'DCIM',
        'config': {
            'models': [
                'dcim.site',
                'dcim.rack',
                'dcim.devicetype',
                'dcim.device',
                'dcim.cable',
            ],
        }
    },
    {
        'widget': 'extras.ObjectCountsWidget',
        'width': 4,
        'height': 2,
        'title': 'Virtualization',
        'config': {
            'models': [
                'virtualization.cluster',
                'virtualization.virtualmachine',
            ]
        }
    },
    {
        'widget': 'extras.ObjectListWidget',
        'width': 12,
        'height': 5,
        'title': 'Change Log',
        'color': 'blue',
        'config': {
            'model': 'core.objectchange',
            'page_size': 25,
        }
    },
]

FIELD_CHOICES = {
    'dcim.Device.status+': (
        ('disposed', 'Disposed of', 'orange'),
        ('unused', 'Active, Unused', 'teal'),
    ),
}

SOCIAL_AUTH_BACKEND_ATTRS = {
    'oidc': (getenv('NB_LOGIN_BUTTON_TEXT', 'Log in with SUSEID'), 'login'),
}
