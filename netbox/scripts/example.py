"""

"""


from dcim.choices import InterfaceTypeChoices
from dcim.models import Device, DeviceRole, Platform, Interface, Cable
from django.core.exceptions import ObjectDoesNotExist
from ipam.choices import IPAddressStatusChoices
from ipam.models import IPAddress, VRF, Prefix, VLAN
from dcim.models import Device, DeviceRole, DeviceType, Site
from tenancy.models import Tenant
from virtualization.choices import VirtualMachineStatusChoices
from virtualization.models import Cluster, VirtualMachine
from extras.scripts import Script, StringVar, IPAddressWithMaskVar
from extras.scripts import ObjectVar, ChoiceVar, IntegerVar, TextVar
from extras.scripts import BooleanVar, MultiObjectVar
from pyzabbix.api import ZabbixAPI
import os
import subprocess
import requests
import time


class New(Script):
    class Meta:
        name = "Create FTTB CPE w/ automatic uplink selection and monitoring"
        description = "Generate standard CPE router configuration \
                       and configure uplink switch and linkage"
        field_order = [
            'business_name',
            'asset_tag',
            'uplink_site',
            'skip_zabbix',
            'skip_uplink_port',
            'confirmation_email',
            'comments',
            'rack_mount']

    # ##################Check to make sure you have these defined##############
    RACK_MOUNT_ID = DeviceType.objects.get(model="RB2011-RM").id
    WALL_MOUNT_ID = DeviceType.objects.get(model="RB2011").id
    SITE_ID = Site.objects.get(name="Customer Premise").id
    DEVICE_ROLE_ID = DeviceRole.objects.get(name="CPE").id
    AGG_ROLE_ID = DeviceRole.objects.get(name="Aggregation").id
    PLATFORM_ID = Platform.objects.get(name="RouterOS").id
    CHOICES = (
        (RACK_MOUNT_ID, "Rack Mount"),
        (WALL_MOUNT_ID, "Wall Mount")
    )
    INET_VLAN = VLAN.objects.get(vid=900)
    MGMT_VLAN = VLAN.objects.get(vid=107)
    SITES = Site.objects.filter(region_id=1)
    ZAPI = ZabbixAPI(
        url='http://172.16.101.51/api_jsonrpc.php/',
        user='Admin',
        password='zabbix')
    SNMP_COMMUNITY = "got"
    # ##################END###################

    rack_mount = ChoiceVar(
        choices=(
            (True, "Rack Mount"), (False, "Wall Mount")))
    business_name = StringVar(label="Business Name")
    asset_tag = StringVar(label="Asset Tag", required=False)
    hardware_choice = ChoiceVar(choices=CHOICES)
    comments = TextVar(label="Comments", required=False)
    uplink_site = ObjectVar(SITES)
    skip_zabbix = BooleanVar(label="Disable Zabbix configuration")
    skip_uplink_port = BooleanVar(label="Disable upstream port selection")
    confirmation_email = BooleanVar(label="Send Confirmation Email")

    def run(self, data, commit):
        # Create the device
        device = Device(
            name=data['business_name'],
            asset_tag=data['asset_tag'],
            device_role_id=self.DEVICE_ROLE_ID,
            device_type_id=data["hardware_choice"],
            platform_id=self.PLATFORM_ID,
            site_id=self.SITE_ID
        )
        device.save()

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
        inet_intf.untagged_vlan = self.INET_VLAN
        inet_intf.save()
        mgmt_intf.save()
        for intf in interfaces:
            intf.enabled = False
            intf.save()
        for intf in enabled_interfaces:
            intf.enabled = True
            intf.mtu = 1500
            intf.save()
        available_ip = Prefix.objects.get(
            vlan=self.MGMT_VLAN).get_first_available_ip()
        ip = IPAddress(
            address=available_ip,
            interface_id=mgmt_intf.id,
            family='4')
        ip.save()
        device.primary_ip4_id = ip.id
        device.primary_ip_id = ip.id
        device.comments = data['comments']
        device.save()

        # ############
        if(not data["skip_zabbix"] and commit):

            # Post to Zabbix API to create host in mikrotik group and ICMP
            # template
            try:
                hostid = self.ZAPI.host.create(
                    host=data["business_name"],
                    interfaces=dict(
                        type=2,
                        main=1,
                        useip=1,
                        ip=available_ip.replace("/24", ""),
                        port=161,
                        dns="",
                        details=dict(
                            version="1",
                            bulk="0",
                            community=self.SNMP_COMMUNITY)
                    ),
                    groups=dict(
                        groupid=15
                    ),
                    templates=dict(
                        templateid=10186
                    )
                )
                self.log_info("zabbix configured successfully")
            except Exception as e:
                self.log_info("failed to configure zabbix {0}".format(e))

        if(not data["skip_uplink_port"] and commit):
            try:
                agg_switches = Device.objects.filter(
                    site=data["uplink_site"],
                    device_role_id=self.AGG_ROLE_ID,
                    status="active")
                selected_interface = ""
                for agg_switch in agg_switches:
                    interfaces = Interface.objects.filter(
                        device_id=agg_switch.id)
                    for interface in interfaces:
                        if (
                            interface.connection_status is not True and
                            interface.enabled is True and
                            interface.description == '' and
                            interface.type == '1000base-x-sfp'
                        ):
                            selected_interface = interface
                            break
                    if selected_interface != "":
                        selected_interface.enabled = True
                        selected_interface.description = device.name
                        selected_interface.mode = "tagged"
                        selected_interface.tagged_vlans.set(
                            [
                                self.INET_VLAN,
                                self.MGMT_VLAN
                            ]
                        )
                        selected_interface.save()
                        cable = Cable(
                            termination_a=uplk_intf,
                            termination_b=selected_interface,
                        )
                        cable.save()
                        self.log_info(
                            "uplink switch chosen. Port {0} on {1}".format(
                                selected_interface.name, agg_switch.name))
                        break
                if selected_interface == "":
                    self.log_failure(
                        "No available aggregate port found. \
                        No aggregate port assigned.")

            except BaseException:
                self.log("failed to document uplink switch")

        self.log_success("Created {0}".format(device.name))
