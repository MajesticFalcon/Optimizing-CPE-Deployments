# Phase 12: Find available uplink port




```python
		agg_switches = Device.objects.filter(site=data["uplink_site"], device_role_id=2, status="active")
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
```