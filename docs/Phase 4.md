# Phase 4: Writing our Ansible playbook

Now that Ansible can talk to Netbox, we need to write a playbook to gather the necessary information and generate the configuration.

There are 5 main tasks we need to acheive. 
1. Get configuration contexts from Netbox
2. Get interfaces that belong to our device
3. Get IP addresses that belong to our device
4. Create a folder to store our configuration
5. Create our configuration

```yaml
---
- hosts: "{{ device_name }}"
  connection: network_cli
  become: no
  gather_facts: no
  vars:
    netbox_url: "https://netbox-server-here"
    netbox_token: token-here
    working_folder: "working-folder-here"
    
  tasks:
    - name: Get config context from Netbox
      uri:
        url: "{{netbox_url}}/api/extras/config-contexts/"
        validate_certs: no
        method: GET
        return_content: yes
        headers:
          accept: "application/json"
          Authorization: "Token {{netbox_token}}"
      register: nb_contexts
      
    - name: Get interfaces for host
      uri:
        url: "{{netbox_url}}/api/dcim/interfaces/?device={{inventory_hostname}}"
        validate_certs: no
        method: GET
        return_content: yes
        headers:
          accept: "application/json"
          Authorization: "Token {{netbox_token}}"
      register: nb_interfaces
      
    - name: Get ip addresses for host
      uri:
        url: "{{netbox_url}}/api/ipam/ip-addresses/?device={{inventory_hostname}}"
        validate_certs: no
        method: GET
        return_content: yes
        headers:
          accept: "application/json"
          Authorization: "Token {{netbox_token}}"
      register: nb_ips
      
    - name: Create folder for {{ inventory_hostname }}
      file:
        dest: "{{working_folder }}/{{inventory_hostname}}"
        state: directory
 ```
 
 We have accomplished goals 1-4, for goal 5, we need to use Jinja templating. Lets use the platform slug to determine the Jinja template for now.
 
 
 Add this to the bottom of the playbook
 ```yaml
    - name: Create configuration file for {{ inventory_hostname }}
      template:
          src: "templates/{{platforms[0]}}.j2"
          dest: "{{working_folder}}/{{inventory_hostname}}/{{inventory_hostname}}.conf"
```
