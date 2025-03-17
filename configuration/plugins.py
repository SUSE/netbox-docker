# Add your plugins and plugin settings here.
# Of course uncomment this file out.

# To learn how to build images with your required plugins
# See https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

# PLUGINS = ["netbox_bgp"]
PLUGINS = [
            'netbox_documents',
            'netbox_healthcheck_plugin',
]

# PLUGINS_CONFIG = {
#   "netbox_bgp": {
#     ADD YOUR SETTINGS HERE
#   }
# }

PLUGINS_CONFIG = {
            'netbox_healthcheck_plugin': {},
            'netbox_documents': {
                'device_documents_location': 'left',
                'enable_circuit_documents': False,
                'enable_circuit_provider_documents': False,
                'enable_device_documents': True,
                'enable_device_type_documents': False,
                'enable_location_documents': False,
                'enable_navigation_menu': False,
                'enable_site_documents': False,
                'enable_vm_documents': False,
            },
}
