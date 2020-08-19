# Phase 3: Configuring Ansible for Netbox

Before we start generating configurations with Ansible, we need to connect Ansible to Netbox. 

In order to pull data from Netbox, we need to generate a token. This can be done in the administrative screen.

For more information on authentication methods visit the [Authentication](https://netbox.readthedocs.io/en/stable/api/authentication/) documentation

Otherwise, generate your token and copy it.

![Phase 3 Token Screen](/img/phase_3_token_screen.PNG)

Now we need to create a yaml configuration file to use as the dynamic inventory for Ansible.

For more information on the netbox plugin, visit the [Netbox Plugin](https://docs.ansible.com/ansible/latest/plugins/inventory/netbox.html) documentation

My configuration file is below
```yaml
---
plugin: netbox
api_endpoint: https://netbox-server-here
token: token-here
validate_certs: False
config_context: True
group_by:
  - device_roles
compose:
  ansible_network_os: platform.slug
```

