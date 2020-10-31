# Phase 12: Find available uplink port

To find the next available port, we need to determine what qualifies as an eligible port and of the eligible ports, which can we actually use.

Requirements: 
	1. This is a downlink connection from and Aggregation switch to an customer CPE on a fiber optic network. We are selling sub-gigabit services, but 1gbps is the perferred connection speed. Therefore, our first requirement is a 1gbps sfp+ interface
	2. We want to make sure the port from the Aggregation switch is unused. You can determine a different method that better suits your business, but if the port is unamed, we consider it unused. Naming the port is apart of our confirmation stage that each service goes through
	3. In addition to not being named, we also check to see the connection status. There is a chance that someone has done one action or the other because that is human error.


Once we find an available port, we want to name it, set it to trunk, set the allowed vlans, and link it to the CPE.

```python

...
		agg_switches = Device.objects.filter(site=data["uplink_site"], device_role_id=DEVICE_ROLE_ID, status="active")
        selected_interface =""
        
        for agg_switch in agg_switches:

            interfaces = Interface.objects.filter(device_id=agg_switch.id)
            for interface in interfaces: 
                if interface.connection_status != True and interface.description == '' and interface.type == '1000base-x-sfp':
                    selected_interface = interface
                    break
            if selected_interface != "":
                selected_interface.enabled = True
                selected_interface.description = device.name
                selected_interface.mode = "tagged"
                selected_interface.tagged_vlans.set(
                    [
                    inet_vlan,
                    mgmt_vlan
                    ]
                )
                selected_interface.save()
                cable = Cable(
                    termination_a= uplk_intf,
                    termination_b= selected_interface,
                )
                cable.save()
                break
...
```