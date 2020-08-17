
# Phase 1: an intuitive interface, that will document our CPE

In Netbox, there is a section for custom scripts. You provide what type of variable will be stored in the database, and Netbox handles the GUI. We know what our variables are, so let’s write the code for the installers to enter them.

*Periods denote code that has been removed from the example and not explained in this document


```python
...
    RACK_MOUNT_ID = DeviceType.objects.get(model="RB2011-RM").id
    WALL_MOUNT_ID = DeviceType.objects.get(model="RB2011").id
    SITE_ID = Site.objects.get(name="Customer Premise").id
    DEVICE_ROLE_ID = DeviceRole.objects.get(name="CPE").id
    CHOICES = (
        (RACK_MOUNT_ID,"Rack Mount"),
        (WALL_MOUNT_ID,"Wall Mount")
    )
...
    business_name = StringVar(label="Business Name")
    hardware_choice = ChoiceVar(choices=CHOICES)
    comments = TextVar(label="Comments", required=False)
```

 The above code, coupled with the required Netbox boiler plate, will give the installer a simple interface like so.
 
 ![Phase 1 Interface](/img/phase%201%20interface.png)
 
The user can enter data, but now we need to create the device and save it to the database and test it.

```python
...
    device = Device(
        name=data['business_name'],
        device_role_id=self.DEVICE_ROLE_ID,
        device_type_id=data["hardware_choice"],
        site_id=self.SITE_ID
    )
    device.save()
...
```
 ![GitHub Logo](/img/phase%201%20device.png)

 
 
