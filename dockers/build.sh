
#FLASK_BUILD
git clone https://github.com/majesticfalcon/schyconf flask_ansible
# cp docker-compose-flask.override.yml flask_ansible/docker-compose.override.yml
docker-compose -f flask_ansible/docker-compose.yml up -d

read -p "Press enter to continue"

#ZABBIX_BUILD

git clone https://github.com/majesticfalcon/zabbix-docker
# cp docker-compose-zabbix.override.yml zabbix-docker/docker-compose.override.yml
docker-compose -f zabbix-docker/docker-compose.yml up -d

read -p "Press enter to continue"

#GITLAB_BUILD
cp docker-compose-gitlab.override.yml gitlab/docker-compose.override.yml
docker-compose -f gitlab/docker-compose.yml up -d

read -p "Press enter to continue"

#NETBOX_BUILD
git clone https://github.com/majesticfalcon/netbox-docker.git
git clone https://github.com/netbox-community/netbox.git netbox-docker/.netbox
cp docker-compose-netbox.override.yml ./netbox-docker/docker-compose.override.yml
sed -i "35i RUN echo \"py-zabbix\" >> /requirements.txt" netbox-docker/Dockerfile
cp -R ../netbox/scripts ./netbox-docker
cp -R ../netbox/initializers ./netbox-docker
# sed -i 's/image: netboxcommunity\/netbox:\${VERSION-latest}/image: netbox_schyconf:1.0/g' ./docker-compose.yml
# sed -i 's/- 8080/- 8000:8080/g' docker-compose.yml
cd netbox-docker/
docker build -t netbox_schyconf:1.0 --build-arg NETBOX_PATH=.netbox --build-arg FROM=python:3.8-alpine .
docker-compose up -d
#######




 
