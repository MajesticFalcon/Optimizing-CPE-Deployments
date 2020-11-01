# Phase 13: Configure Aggregation Switchport

Now that we have found an appropriate switchport to use, we can begin writing the code to configure it.

Draft flow:

1. User creates device
2. Uplink switch and port are configured in netbox
3. The webhook from netbox device creation calls an API
4. API calls Ansible playbook using details from Webhook/API
