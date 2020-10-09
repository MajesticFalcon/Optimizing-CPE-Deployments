# Phase 11: Integrate with Zabbix monitoring system

The last step is to add the device to the monitoring system where ICMP statistics, interface optic levels and more begin to be recorded.


1. Add py-zabbix to netbox requirements.txt
2. Install py-zabbix
3. Connect to API
4. Create host with host group and template

```bash
echo "py-zabbix==1.1.5" >> /opt/netbox/requirements.txt
source /opt/netbox/netbox/venv/bin/activate
pip install -r /opt/netbox/requirements.txt
```

In your script you should now be able to utilize the API package

```python
...

    ZAPI = ZabbixAPI(url='http://_____/api_jsonrpc.php/', user='Admin', password='zabbix')

...
  
    hostid = self.ZAPI.host.create(
            host=data['business_name'],
            interfaces=dict(
                type=2,
                main=1,
                useip=1,
                ip=available_ip.replace("/24",""),
                port=161,
                dns="",
                details=dict(
                    version="1", 
                    bulk="0",
                    community="gofast89")
                ),
            groups=dict(
                groupid=15
                ),
            templates=dict(
                templateid=10186
                )
            )
    
```

The groupid and templateid can be found by browsing to each respectively and investigating the URL. Alternatively, you can pragmatically determine the ids by making more api calls.

The above configuration assumes you are using SNMP. For more information about host creation, visit the zabbix <a href="https://www.zabbix.com/documentation/current/manual/api/reference/host/create">documentation </a>

If you are using Zabbix 5.0, don't forget about the "details" array that is now required with API calls.
