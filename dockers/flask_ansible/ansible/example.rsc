:delay 30s
/interface bridge
add name=b107 protocol-mode=none
add name=b349 protocol-mode=none
/interface ethernet
set [ find default-name=ether1 ] name="ether1 - Internet"
set [ find default-name=ether10 ] name="ether10 - Uplink"
/interface vlan
add interface="ether10 - Uplink" name=ether10v107 vlan-id=107
add interface="ether10 - Uplink" name=ether10v349 vlan-id=349
/interface wireless security-profiles
set [ find default=yes ] supplicant-identity=MikroTik
/queue type
set 1 pfifo-limit=2048
/queue interface
set "ether1 - Internet" queue=ethernet-default
set ether2 queue=ethernet-default
set ether3 queue=ethernet-default
set ether4 queue=ethernet-default
set ether5 queue=ethernet-default
set ether6 queue=ethernet-default
set ether7 queue=ethernet-default
set ether8 queue=ethernet-default
set ether9 queue=ethernet-default
set "ether10 - Uplink" queue=ethernet-default
/interface bridge port
add bridge=b349 interface="ether1 - Internet"
add bridge=b107 interface=ether10v107
add bridge=b349 interface=ether10v349
/ip neighbor discovery-settings
set discover-interface-list=none
/ip address
add address=10.0.7.5/24 interface=b107 network=10.0.7.0
/ip firewall filter
add action=accept chain=input comment=Management src-address=99.99.99.0/24
add action=accept chain=output dst-address=99.99.99.0/24
add action=accept chain=input comment=NTP protocol=udp src-address=99.99.99.2 \
    src-port=123
add action=accept chain=output comment=SYSLOG dst-address=99.99.99.3
/ip route
add distance=1 gateway=99.99.99.1
/ip service
set telnet disabled=yes
set ftp disabled=yes
set www disabled=yes
set api disabled=yes
set api-ssl disabled=yes
/system identity
set name=HardysCheckpoint
/system logging
add action=disk topics=critical
/system ntp client
set enabled=yes primary-ntp=99.99.99.2
/tool bandwidth-server
set enabled=no
/tool graphing resource
add allow-address=99.99.99.0/24
/tool mac-server
set allowed-interface-list=none
/tool mac-server mac-winbox
set allowed-interface-list=none
/tool mac-server ping
set enabled=no

