from core.models import ObjectType
from users.models import Group, ObjectPermission
from django.apps import apps

groups = {
        'admins': None,
        'default-users': None,
}

for group in Group.objects.all():
    if group.name not in groups:
        group.delete()

for group in groups:
    groups[group], _ = Group.objects.get_or_create(name=group)

def name_to_object(name: str):
    try:
        model = apps.get_model(name)
    except LookupError:
        return None
    return ObjectType.objects.get_for_model(model)

def create_permission(name: str, actions: set[str], objects: set[str], groups: set[Group]):
    # Check if it already exists
    objectpermission, _ = ObjectPermission.objects.update_or_create(
        name=name,
        defaults={'actions': list(actions)},
    )
    objectpermission.object_types.set([ name_to_object(x) for x in objects if  name_to_object(x) is not None])
    # Save to make sure the object has an id before adding group relationships
    objectpermission.save()
    for group in groups:
        objectpermission.groups.add(group)
    # Save the relationships now
    objectpermission.save()
    return objectpermission


common_objects = {
    'circuits.circuit',
    'circuits.circuitgroup',
    'circuits.circuitgroupassignment',
    'circuits.circuittermination',
    'circuits.circuittype',
    'circuits.provider',
    'circuits.provideraccount',
    'circuits.providernetwork',
    'circuits.virtualcircuit',
    'circuits.virtualcircuittermination',
    'circuits.virtualcircuittype',
    'dcim.cable',
    'dcim.cablepath',
    'dcim.cabletermination',
    'dcim.consoleport',
    'dcim.consoleporttemplate',
    'dcim.consoleserverport',
    'dcim.consoleserverporttemplate',
    'dcim.devicebay',
    'dcim.devicebaytemplate',
    'dcim.devicerole',
    'dcim.devicetype',
    'dcim.frontport',
    'dcim.frontporttemplate',
    'dcim.interface',
    'dcim.interfacetemplate',
    'dcim.inventoryitem',
    'dcim.inventoryitemrole',
    'dcim.inventoryitemtemplate',
    'dcim.location',
    'dcim.macaddress',
    'dcim.manufacturer',
    'dcim.module',
    'dcim.modulebay',
    'dcim.modulebaytemplate',
    'dcim.moduletype',
    'dcim.platform',
    'dcim.powerfeed',
    'dcim.poweroutlet',
    'dcim.poweroutlettemplate',
    'dcim.powerpanel',
    'dcim.powerport',
    'dcim.powerporttemplate',
    'dcim.rack',
    'dcim.rackreservation',
    'dcim.rackrole',
    'dcim.racktype',
    'dcim.rearport',
    'dcim.rearporttemplate',
    'dcim.region',
    'dcim.site',
    'dcim.sitegroup',
    'dcim.virtualchassis',
    'dcim.virtualdevicecontext',
    'django_rq.queue',
    'extras.customfieldchoiceset',
    'extras.exporttemplate',
    'extras.imageattachment',
    'extras.journalentry',
    'extras.savedfilter',
    'ipam.aggregate',
    'ipam.asn',
    'ipam.asnrange',
    'ipam.ipaddress',
    'ipam.iprange',
    'ipam.prefix',
    'ipam.rir',
    'ipam.role',
    'ipam.routetarget',
    'ipam.service',
    'ipam.servicetemplate',
    'ipam.vlan',
    'ipam.vlangroup',
    'ipam.vlantranslationpolicy',
    'ipam.vlantranslationrule',
    'ipam.vrf',
    'tenancy.contact',
    'tenancy.contactassignment',
    'tenancy.contactgroup',
    'tenancy.contactrole',
    'virtualization.cluster',
    'virtualization.clustergroup',
    'virtualization.clustertype',
    'virtualization.virtualdisk',
    'virtualization.vminterface',
}

protected_objects = {
    'dcim.device',
    'virtualization.virtualmachine',
}

root_objects = common_objects | protected_objects | {
    'core.autosyncrecord',
    'core.configrevision',
    'core.datafile',
    'core.datasource',
    'core.job',
    'core.managedfile',
    'core.objectchange',
    'core.objecttype',
    'db.testmodel',
    'extras.bookmark',
    'extras.cachedvalue',
    'extras.configcontext',
    'extras.configtemplate',
    'extras.customfield',
    'extras.customlink',
    'extras.dashboard',
    'extras.eventrule',
    'extras.notification',
    'extras.notificationgroup',
    'extras.script',
    'extras.scriptmodule',
    'extras.subscription',
    'extras.tag',
    'extras.taggeditem',
    'extras.webhook',
    'ipam.fhrpgroup',
    'ipam.fhrpgroupassignment',
    'social_django.association',
    'social_django.code',
    'social_django.nonce',
    'social_django.partial',
    'social_django.usersocialauth',
    'tenancy.tenant',
    'tenancy.tenantgroup',
    'users.group',
    'users.objectpermission',
    'users.token',
    'users.user',
    'vpn.ikepolicy',
    'vpn.ikeproposal',
    'vpn.ipsecpolicy',
    'vpn.ipsecprofile',
    'vpn.ipsecproposal',
    'vpn.l2vpn',
    'vpn.l2vpntermination',
    'vpn.tunnel',
    'vpn.tunnelgroup',
    'vpn.tunneltermination',
    'wireless.wirelesslan',
    'wireless.wirelesslangroup',
    'wireless.wirelesslink',
}

user_rw_objects = common_objects.union({
    'netbox_documents.devicedocument',
    'netbox_documents.devicetypedocument',
    'netbox_documents.locationdocument',
    'netbox_documents.sitedocument',
    'netbox_documents.vmdocument',
})

user_ro_objects = {
    'extras.customfield',
    'extras.tag',
    'tenancy.tenant',
    'tenancy.tenantgroup',
}

actions_edit = {'view', 'add', 'change'}

permissions = {
        'root': {
            'actions': actions_edit,
            'objects': root_objects,
            'groups': {groups['admins']},
        },
        'user-rw': {
            'actions': actions_edit,
            'objects': protected_objects,
            'groups': {groups['default-users']},
        },
        'user-rwd': {
            'actions': actions_edit | {'delete'},
            'objects': user_rw_objects,
            'groups': {groups['default-users']},
        },
        'user-ro': {
            'actions': {'view'},
            'objects': user_ro_objects,
            'groups': {groups['default-users']},
        },
}

for permission in ObjectPermission.objects.all():
    if permission.name not in permissions:
        permission.delete()

for permission, permission_data in permissions.items():
    create_permission(
            name=permission,
            **permission_data,
    )
