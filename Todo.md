# Optimizing-CPE-Deployments
Automate the logistics surrounding new customer installations

### Todo
- [ ] Configure uplink switch port using Ansible and Flask
- [ ] Optionally send syslog event to server or file to indicate completion
- [ ] Design auto configuration application process 
  - [ ] Special VLAN for configuration
  - [ ] Python loop searching for new device on ethernet segment
  - [ ] Verify the identity of the new device
  - [ ] Reset and apply configuration to new device
  - [ ] Play beep code on new device to indicate success
- [ ] Dockerize project to allow for anybody to replicate environment
  - [ ] Docker-compose project including the following managed containers
    - [ ] Database
    - [ ] Netbox
    - [ ] Zabbix
    - [ ] Gitlab
    - [ ] Syslog
- [ ] Upload code for scripts to allow for easy adoption
  - [ ] Sanitize code
  - [ ] Add comments
- [ ] Add asset tag
- [ ] Add secret
- [ ] Add optional tag


### In Progress
- [ ] Daemonize Flask
- [ ] Use git for application files. Ansible, Flask, Netbox scripts, etc.
- [ ] Optionally send email to indicate completion 


### Done ✓
- [x] Simple GUI to document CPE
- [x] Simple GUI that applies organization parameters
- [x] Find next available IP in Mgmt pool
- [x] Generate configuration using Ansible and Jinja
- [x] Create Flask app
- [x] Create Webhook
- [x] Create custom button in Netbox
- [x] Integrate with Zabbix
- [x] Find next available uplink switch port and configure Netbox
- [x] Add Flask app code
- [x] Connect comments box to device comments
- [x] Add indications if either Zabbix, Gitlab, Ansible, or other dependancy fails
- [x] Add option to select uplink port automatically. Set as default
- [x] Only configure zabbix if checkbox is checked

