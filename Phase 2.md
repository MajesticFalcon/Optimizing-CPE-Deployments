
# Phase 2: Document device with specific organizational parameters 

Our standard configuration has the following:

1.	Trunk interface (highest numbered port)
2.	Access interface (lowest numbered port)
3.	Management IP on SVI
4.	Identity
5.	Named Uplink and Downlink ports
6.	Data VLAN
7.	Management VLAN
8.	All unused ports are disabled

We need to add these variables to our device so they can be used to generate a configuration later. The next section requires some setup to be defined in Netbox’s device type template.

1.	Interfaces must be names like they are in Mikrotik default names
    1.	ether1, ether2, etc
2.	Mikrotik must have an interface defined for the SVI.

```python
...
    INET_VLAN_ID_ID = VLAN.objects.get(vid=900)
    MGMT_VLAN_ID_ID = VLAN.objects.get(vid=107)
...
        interfaces = Interface.objects.filter(device_id=device.id)
        enabled_interfaces = []
        mgmt_intf = interfaces.get(name="b107")
        enabled_interfaces.append(mgmt_intf)
        uplk_intf = interfaces.get(name="ether10")
        enabled_interfaces.append(uplk_intf)
        uplk_intf.mode = "tagged"
        uplk_intf.tagged_vlans.set(
            [
            self.INET_VLAN,
            self.MGMT_VLAN
            ]
        )
        uplk_intf.description = "Uplink"
        uplk_intf.save()
        inet_intf = interfaces.get(name="ether1")
        enabled_interfaces.append(inet_intf)
        inet_intf.description = "Internet"
        inet_intf.mode = "access"
        inet_intf.untagged_vlan=self.INET_VLAN
        inet_intf.save()
        mgmt_intf.save()
        for intf in interfaces:
          intf.enabled = False
          intf.save()
        for intf in enabled_interfaces:
          intf.enabled = True
          intf.mtu = 1500
          intf.save()
        available_ip = Prefix.objects.get(vlan=self.MGMT_VLAN).get_first_available_ip()
        ip = IPAddress(address=available_ip, interface_id=mgmt_intf.id, family='4')
        ip.save()
        device.primary_ip4_id=ip.id
        device.primary_ip_id=ip.id
        device.save()
```

Similar to phase 1, we get a new device, but now our device has our standard configuration on it and an available IP has been selected from a pool of IP addresses.

![Phase 2 Devices](/img/phase%202%20devices.png)

And the device specific parameters have been created

![Phase 2 Interfaces](/img/phase%202%20interfaces.png)


