#!/bin/sh -efu

exec \
	/opt/netbox/venv/bin/gunicorn \
	--bind 0.0.0.0:8080 \
	--config /opt/netbox/netbox-git/contrib/gunicorn.py \
	--pythonpath /opt/netbox/netbox \
	--workers $(( $(nproc) + 1 )) \
	netbox.wsgi
