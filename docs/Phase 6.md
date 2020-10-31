# Phase 6: Checkpoint. Let's recap and test what we have done so far.

1. We have created a custom Netbox script that creates an simple and intuitive web interface for installers to enter the minimum required information to install a circuit
2. The script creates a device in Netbox and applies our organizational specific parameters
3. We have generated a special token that will allow Ansible access to Netbox. We have used this token in the Netbox Ansible plugin and tested our connectivity to the Netbox DB
4. We have written an Ansible playbook that gathers the required information for our Jinja template
5. We wrote a Jinja configuration template that incorporates all of our requirements for a CPE

To do:


1. Create an api end point or utilize existing automation to call the Ansible playbook
2. Create a webhook to call our web end point when a device in Netbox is created
3. Push configuration to gitlab
4. Add custom button in Netbox to view/download the configuration from Gitlab

At this point you should be able to do the following:

1. Create a device using a custom script
2. Pull devices into Ansible using the Netbox plugin
3. Run an Ansible playbook and generate a configuration file

```bash
ansible-inventory -i netbox_inventory.yml  --list 
```

and get something like this

```
{
    "_meta": {
        "hostvars": {
            "Phase 1 Example Device": {
                "config_context": [
                    {
                        "gateway": "99.99.99.1",
                        "management_networks": "99.99.99.0/24",
                        "ntp_server": "99.99.99.2",
                        "syslog_server": "99.99.99.3"
                    }
                ],
                "device_roles": [
                    "CPE"
                ],
                "device_types": [
                    "RB2011-RM"
                ],
                "manufacturers": [
                    "Mikrotik"
                ],
                "sites": [
                    "Customer Premise"
                ]
            },
            "Phase 2 Example Device": {
                "ansible_host": "10.0.7.1",
                "config_context": [
                    {
                        "gateway": "99.99.99.1",
                        "management_networks": "99.99.99.0/24",
                        "ntp_server": "99.99.99.2",
                        "syslog_server": "99.99.99.3"
                    }
                ],
                "device_roles": [
                    "CPE"
                ],
                "device_types": [
                    "RB2011-RM"
                ],
                "manufacturers": [
                    "Mikrotik"
                ],
                "primary_ip4": "10.0.7.1",
                "sites": [
                    "Customer Premise"
                ]
            }
        }
    },
    "all": {
        "children": [
            "device_roles_CPE",
            "ungrouped"
        ]
    },
    "device_roles_CPE": {
        "hosts": [
            "Phase 1 Example Device",
            "Phase 2 Example Device"
        ]
    }
}
```

and if you have configured a device, you should be able to run the playbook we created and get a configuration file

```
  ansible-playbook -i ./netbox_inventory.yml create_configuration.yml -e "device_name=Phase1 ansible_network_os=routeros"
```

and get something similar below

```
PLAY [Phase2] **********************************************************************************************************************

TASK [Get config context from Netbox] **********************************************************************************************
[DEPRECATION WARNING]: Distribution Ubuntu 18.04 on host Phase2 should use /usr/bin/python3, but is using /usr/bin/python for
backward compatibility with prior Ansible releases. A future Ansible release will default to using the discovered platform python
for this host. See https://docs.ansible.com/ansible/2.9/reference_appendices/interpreter_discovery.html for more information. This
feature will be removed in version 2.12. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [Phase2]

TASK [Get device from Netbox] ******************************************************************************************************
ok: [Phase2]

TASK [Get interfaces for host] *****************************************************************************************************
ok: [Phase2]

TASK [Get ip addresses for host] ***************************************************************************************************
ok: [Phase2]

TASK [Create temp folder for Phase2] ***********************************************************************************************
changed: [Phase2]

TASK [Create configuration file for Phase2] ****************************************************************************************
[WARNING]: File '/docker/git/Phase2/Phase2.conf' created with default permissions '600'. The previous default was '666'. Specify
'mode' to avoid this warning.
changed: [Phase2]

PLAY RECAP *************************************************************************************************************************
Phase2                     : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```


