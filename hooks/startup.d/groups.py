from core.models import ObjectType
from users.models import Group, ObjectPermission
from django.apps import apps

group_admins, _ = Group.objects.get_or_create(name='admins')
group_users, _ = Group.objects.get_or_create(name='default-users')

group_admins.save()
group_users.save()

def name_to_object(name: str):
    try:
        model = apps.get_model(name)
    except LookupError:
        return None
    return ObjectType.objects.get_for_model(model)

def create_permission(name: str, actions: set[str], objects: set[str], groups: set[Group]):
    # Check if it already exists
    objectpermission,_ = ObjectPermission.objects.get_or_create(
        name=name,
        actions=list(actions),
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
    'dcim.poweroutlettemplate',
    'tenancy.contact',
    'dcim.inventoryitemtemplate',
    'dcim.device',
    'dcim.rack',
    'virtualization.cluster',
    'dcim.devicebaytemplate',
    'dcim.platform',
    'dcim.cabletermination',
    'dcim.interface',
    'ipam.vlan',
    'dcim.rearport',
    'dcim.frontporttemplate',
    'dcim.frontport',
    'dcim.sitegroup',
    'dcim.cablepath',
    'dcim.site',
    'circuits.virtualcircuittype',
    'extras.journalentry',
    'dcim.inventoryitem',
    'dcim.powerporttemplate',
    'dcim.moduletype',
    'dcim.poweroutlet',
    'extras.exporttemplate',
    'extras.imageattachment',
    'virtualization.clustergroup',
    'ipam.prefix',
    'ipam.asn',
    'dcim.virtualchassis',
    'dcim.modulebaytemplate',
    'ipam.asnrange',
    'circuits.virtualcircuittermination',
    'ipam.iprange',
    'dcim.consoleport',
    'extras.customfieldchoiceset',
    'circuits.providernetwork',
    'circuits.circuitgroupassignment',
    'dcim.inventoryitemrole',
    'dcim.rearporttemplate',
    'circuits.provider',
    'virtualization.clustertype',
    'circuits.circuittermination',
    'dcim.racktype',
    'dcim.powerport',
    'ipam.servicetemplate',
    'circuits.circuittype',
    'dcim.interfacetemplate',
    'dcim.rackreservation',
    'dcim.module',
    'ipam.vlantranslationpolicy',
    'circuits.provideraccount',
    'dcim.devicebay',
    'dcim.cable',
    'ipam.vlangroup',
    'dcim.consoleserverporttemplate',
    'tenancy.contactassignment',
    'virtualization.virtualmachine',
    'ipam.routetarget',
    'dcim.manufacturer',
    'virtualization.virtualdisk',
    'dcim.powerpanel',
    'circuits.circuit',
    'dcim.rackrole',
    'tenancy.contactrole',
    'dcim.macaddress',
    'ipam.rir',
    'dcim.consoleporttemplate',
    'tenancy.contactgroup',
    'circuits.circuitgroup',
    'dcim.region',
    'ipam.aggregate',
    'dcim.devicetype',
    'ipam.vlantranslationrule',
    'dcim.modulebay',
    'dcim.virtualdevicecontext',
    'extras.savedfilter',
    'dcim.location',
    'virtualization.vminterface',
    'circuits.virtualcircuit',
    'ipam.ipaddress',
    'ipam.vrf',
    'django_rq.queue',
    'dcim.consoleserverport',
    'ipam.service',
    'dcim.powerfeed',
    'ipam.role',
    'dcim.devicerole'
}

root_objects = common_objects.union({
    'extras.webhook',
    'extras.customlink',
    'core.datafile',
    'extras.eventrule',
    'extras.dashboard',
    'extras.notificationgroup',
    'vpn.tunneltermination',
    'users.objectpermission',
    'users.user',
    'vpn.l2vpntermination',
    'social_django.code',
    'vpn.ikepolicy',
    'tenancy.tenantgroup',
    'db.testmodel',
    'extras.cachedvalue',
    'core.datasource',
    'core.objecttype',
    'users.token',
    'vpn.l2vpn',
    'users.group',
    'vpn.tunnel',
    'vpn.ipsecprofile',
    'wireless.wirelesslink',
    'extras.script',
    'extras.configcontext',
    'social_django.nonce',
    'core.objectchange',
    'core.managedfile',
    'vpn.ipsecproposal',
    'wireless.wirelesslan',
    'social_django.partial',
    'vpn.tunnelgroup',
    'extras.tag',
    'core.configrevision',
    'extras.notification',
    'tenancy.tenant',
    'social_django.association',
    'ipam.fhrpgroupassignment',
    'wireless.wirelesslangroup',
    'ipam.fhrpgroup',
    'extras.configtemplate',
    'vpn.ipsecpolicy',
    'extras.bookmark',
    'core.job',
    'extras.customfield',
    'extras.subscription',
    'vpn.ikeproposal',
    'extras.scriptmodule',
    'extras.taggeditem',
    'social_django.usersocialauth',
    'core.autosyncrecord'
})

user_rw_objects = common_objects.union({
    'netbox_documents.devicetypedocument',
    'netbox_documents.sitedocument',
    'netbox_documents.vmdocument',
    'netbox_documents.locationdocument',
    'netbox_documents.devicedocument'}
)

user_ro_objects = {
    'extras.tag',
    'extras.customfield',
    'tenancy.tenantgroup',
    'tenancy.tenant'
}

actions_readonly = {'view'}
actions_edit = {'view', 'add', 'change', 'delete' }

create_permission(name='root', actions=actions_edit, objects=root_objects, groups={group_admins})
create_permission(name='user-rw', actions=actions_edit, objects=user_rw_objects, groups={group_users})
create_permission(name='user-ro', actions=actions_readonly, objects=user_ro_objects, groups={group_users})
