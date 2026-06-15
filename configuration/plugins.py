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
                'enable_navigation_menu': False,
                'documents_location': 'left',

                'custom_doc_types': [
                    ('datasheet', 'Data Sheet', 'green'),
                    ('invoice', 'Invoice', 'gold'),
                    ('manual', 'Manual', 'pink'),
                    ('packingslip', 'Packing Slip', 'grey'),
                    ('purchaseorder', 'Purchase Order', 'orange'),
                    ('quote', 'Quote', 'silver'),
                    ('service', 'Service Agreement', 'blue'),
                    ('warranty', 'Warranty information or RMA', 'red'),
                ],

                'allowed_doc_types': {
                    '__all__': [],
                    'dcim.device': [
                        'datasheet',
                        'invoice',
                        'manual',
                        'packingslip',
                        'purchaseorder',
                        'quote',
                        'service',
                        'warranty',
                    ],
                },

            },
}
