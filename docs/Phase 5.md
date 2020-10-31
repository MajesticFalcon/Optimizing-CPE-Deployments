# Phase 5: Writing our Jinja template

In our environment, we primary deploy Mikrotiks. This section will provide an example on how to accomplish our goals using Mikrotik, but any vendor could be used here

Jinja is a templating language that will allow us to model our configuration using Python. In my "hot-n-ready" configuration, there are a lot of settings that need to be applied.

See [Securing your Mikrotik](https://wiki.mikrotik.com/wiki/Manual:Securing_Your_Router) for more information on hardening your configurations

1. Set the name of the device

    ```/system identity set name={{inventory_hostname}}```
2. Enable graphing on the internet interface from mgmt networks

    ```/tool graphing interface add allow-address={{nb_contexts.json.results[0].data.management_networks}} interface={{inf.name}}```
3. Set the name and description in the standard format, if the name and description exist

    ```/interface ethernet set [ find default-name={{intf.name}} ] name="{{int.name}} - {{intf.description}}"```
4. Configure management bridge

    ```/interface bridge add name={{intf.name}} protocol-mode=none```
5. Configure management IPs

    ```/ip address add address={{address.addresss}} interface={{intf.name}}```
6. Configure tagged interfaces

    ```/interface bridge add name=b{{vlan.vid}} protocol-mode=none
    /interface vlan add vlan-id={{vlan.vid}} name={{intf.name}}v{{vlan.vid}} interface={{intf.name}}
    /interface bridge port add interface={{intf.name}}v{{vlan.vid}} bridge=b{{vlan.vid}}```
7. Configure untagged interfaces

    ```
      /interface bridge add name=b{{intf.untagged_vlan.vid}} protocol-mode=none
      /interface bridge port add interface={{intf.name}} bridge=b{{intf.untagged_vlan.vid}}```
8. Set the ethernet queues

    ```/queue interface set {{intf.name}} queue=ethernet-default```
9. Set queue buffer

    ```/queue type set 1 pfifo-limit=2048```
10. Disable discovery on all interfaces

    ```/ip neighbor discovery-settings set discover-interface-list=none```
11. Configure default firewall rules

    ```
      /ip firewall filter 
      add action=accept chain=input comment=Management src-address={{ nb_contexts.json.results[0].data.management_networks}}
      add action=accept chain=output dst-address={{ nb_contexts.json.results[0].data.management_networks}}
      add action=accept chain=input comment=NTP protocol=udp src-address={{nb_contexts.json.results[0].data.ntp_server}} src-port=123
      add action=accept chain=output comment=SYSLOG dst-address={{ nb_contexts.json.results[0].data.syslog_server }}
      #Dont add these rules yet
      #add action=drop chain=input
      #add action=drop chain=output
      #add action=drop chain=forward
      ```
 12. Add default gateway for this management network
    ```
      /ip route
      add gateway={{ nb_contexts.json.results[0].data.gateway}}```
 13. Disable unused services
    ```
      /ip service
      set telnet disabled=yes
      set ftp disabled=yes
      set www disabled=yes
      set api disabled=yes
      set api-ssl disabled=yes```
14. Configure remote logging
    ```
      /system logging action
      set 3 remote={{ nb_contexts.json.results[0].data.syslog_server }}
      /system logging
      add action=remote topics=info```
15. Configure NTP
    ```
      /system ntp client
      set enabled=yes primary-ntp={{nb_contexts.json.results[0].data.ntp_server}}```
16. Disable bandwidth server
    ```
      /tool bandwidth-server
      set enabled=no```
17. Configure resource graphing access from management networks
    ```
      /tool graphing resource
      add allow-address={{ nb_contexts.json.results[0].data.management_networks}}```
18. Disable l2 management services
    ```
      /tool mac-server
      set allowed-interface-list=none
      /tool mac-server mac-winbox
      set allowed-interface-list=none
      /tool mac-server ping
      set enabled=no```


If we translate those goals into Jinja, we get the following file. Save it in working_dir/templates/RouterOS.j2

```jinja
/system identity set name={{inventory_hostname}}
{% for intf in nb_interfaces.json.results %}
{%   if intf.description == "internet" %}
/tool graphing interface
add allow-address={{nb_contexts.json.results[0].data.management_networks}} interface={{intf.name}}
{%   endif %}
{%   if intf.description != "" and intf.type.value != "virtual" %}
/interface ethernet set [ find default-name={{ intf.name }} ] name="{{ intf.name }} - {{ intf.description }}"
{%   endif %}
{%   if intf.type.value == "virtual" %}
/interface bridge add name={{ intf.name }} protocol-mode=none
{%   endif %}
{%   for address in nb_ips.json.results %}
{%     if address.interface.name == intf.name %}
/ip address add address={{ address.address }} interface={{ intf.name }}
{%     endif %}
{%   endfor %}
{%   if intf.mode != None %}
{%     if intf.mode.value == "tagged" %}
{%       for vlan in intf.tagged_vlans %}
/interface bridge add name=b{{vlan.vid}} protocol-mode=none
/interface vlan add vlan-id={{vlan.vid}} name={{intf.name}}v{{vlan.vid}} interface={{intf.name}}
/interface bridge port add interface={{intf.name}}v{{vlan.vid}} bridge=b{{vlan.vid}}
{%       endfor %}
{%     elif intf.mode.value == "access" %}
/interface bridge add name=b{{intf.untagged_vlan.vid}} protocol-mode=none
/interface bridge port add interface={{intf.name}} bridge=b{{intf.untagged_vlan.vid}}
{%     endif %}
{%   endif %}
/queue interface set {{intf.name}} queue=ethernet-default
{%   endfor %}
/queue type set 1 pfifo-limit=2048
/ip neighbor discovery-settings set discover-interface-list=none
/ip firewall filter 
add action=accept chain=input comment=Management src-address={{ nb_contexts.json.results[0].data.management_networks}}
add action=accept chain=output dst-address={{ nb_contexts.json.results[0].data.management_networks}}
add action=accept chain=input comment=NTP protocol=udp src-address={{nb_contexts.json.results[0].data.ntp_server}} src-port=123
add action=accept chain=output comment=SYSLOG dst-address={{ nb_contexts.json.results[0].data.syslog_server }}
#Dont add these rules yet
#add action=drop chain=input
#add action=drop chain=output
#add action=drop chain=forward
/ip route
add gateway={{ nb_contexts.json.results[0].data.gateway}}
/ip service
set telnet disabled=yes
set ftp disabled=yes
set www disabled=yes
set api disabled=yes
set api-ssl disabled=yes
/system logging
add action=disk topics=critical
/system ntp client
set enabled=yes primary-ntp={{nb_contexts.json.results[0].data.ntp_server}}
/tool bandwidth-server
set enabled=no
/tool graphing resource
add allow-address={{ nb_contexts.json.results[0].data.management_networks}}
/tool mac-server
set allowed-interface-list=none
/tool mac-server mac-winbox
set allowed-interface-list=none
/tool mac-server ping
set enabled=no
```
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
