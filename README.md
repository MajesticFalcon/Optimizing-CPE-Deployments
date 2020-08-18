


# A Primer for Optimizing FTTx CPE Deployments Using Free and Open Source Software

In this project, I explore a potential method for allowing installation crews to generate their own configurations at will. The goal is to remove the technical nature of preparing CPE equipment, device management software, and monitoring services. 

### Examining the problem
There has been a growing problem regarding CPE availability now that office staff work from home. The installer teams must request the list of CPEs well in advance to give our technicians ample time to schedule in office visits. The procedure looks like this.

1.	An install team schedules fiber optic installs for x number of businesses a week in advance. The list of businesses is given to the office staff.
2.	A technician schedules a day to drive into the office and configure switches
3.	A technician gathers information regarding each individual circuit
    1.	Management network
    2.	Available IP, vlan, firewall
    3.	POP
    4.	Uplink switch
    5.	Available uplink port
    6.	Identification
    7.	Name, location, package
    8.	Demarcation
    9.	Mounting options
4.	Based on the above variables the technician will:
    1.	Decide which Mikrotik will be deployed
    2.	Apply a “hot-n-ready” configuration
    3.	Change circuit specific settings
    4.	Test the device
    5.	Add device central monitoring server
    6.	Add device into device management server
    7.	Hand off the device 
    8.	Configure the uplink switch port for circuit specific information
    9.	Update device management server

The procedure is not complex or all that difficult in general and has a well-defined SOP. This is a great example of a process that can be automated. 

### Alternatives

There are many different deployments we could switch to, we could use a media converter instead of a managed switch, we could use some sort of automated configuration protocol like TR-69, we could use a proprietary vendor solution for ZTP, or we could change our deployment processes to facilitate a different procedure all together. Given our existing environment, I propose an additional option.

### Proposed solution

What if we could give the install crews the power to generate configurations with a simple interface without changing the network, the physical install processes, or the equipment? The process could look something like this:

1.	An install team schedules fiber optic installs for x number of businesses a week in advance
2.	The install team visits a webpage and enters in required fields
3.	The webpage updates device management software, monitoring software, builds a configuration based on the fields entered and configures the uplink switch
4.	The webpage provides the configuration, uplink switch port, and confirmation the device has been documented and monitored

We don’t want or need the installers to know how to configure a Mikrotik, they only need to know how to upload a configuration which is a reasonable request.

### Required software

To accomplish these goals, we can utilize the following:
1.	Netbox
2.	Ansible
3.	Zabbix
4.	Python

*This primer won’t detail how any of these services work, but instead how they may be utilized to accomplish the task above.

[Phase 1: An intuitive interface that will document our CPE](https://github.com/MajesticFalcon/Optimizing-CPE-Deployments/blob/master/Phase%201.md)

[Phase 2: Document device with specific organizational parameters ](https://github.com/MajesticFalcon/Optimizing-CPE-Deployments/blob/master/Phase%202.md)

