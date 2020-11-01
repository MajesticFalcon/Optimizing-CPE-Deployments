---
name: Housekeeping
about: A change pertaining to the codebase itself
title: ''
labels: ''
assignees: ''

---

### Proposed Changes
Transition Netbox from native linux installation to docker installation. Then provide the relevant commands in the docker folder similar to Zabbix and Gitlab.

<!-- Provide justification for the proposed change(s). -->
### Justification
In order for a user to utilize this project, they will need to install and configure Netbox. This can lead to slight changes in installation and ultimately the possibility of an incompatible install. Additionally, the project currently uses an old version of Netbox, moving to docker will allow for better paths to upgrades and maintenance.
