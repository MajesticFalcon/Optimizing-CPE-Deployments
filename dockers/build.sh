
#FLASK_BUILD
cp docker-compose-flask.override.yml flask_ansible/docker-compose.override.yml
docker-compose -f flask_ansible/docker-compose.yml up -d

read -p "Press enter to continue"

#ZABBIX_BUILD
git clone https://github.com/zabbix/zabbix-docker
# cd zabbix-docker
# git checkout 4.2
# cd ..
cp docker-compose-zabbix.override.yml zabbix-docker/docker-compose.override.yml
cp zabbix-docker/docker-compose_v3_ubuntu_mysql_latest.yaml zabbix-docker/docker-compose.yml
docker-compose -f zabbix-docker/docker-compose.yml up -d

read -p "Press enter to continue"

#GITLAB_BUILD
cp docker-compose-gitlab.override.yml gitlab/docker-compose.override.yml
docker-compose -f gitlab/docker-compose.yml up -d

read -p "Press enter to continue"

#NETBOX_BUILD
git clone https://github.com/netbox-community/netbox-docker.git
git clone https://github.com/netbox-community/netbox.git netbox-docker/.netbox
cp docker-compose-netbox.override.yml ./netbox-docker/docker-compose.override.yml
sed -i "35i RUN echo \"py-zabbix\" >> /requirements.txt" netbox-docker/Dockerfile
# sed -i 's/image: netboxcommunity\/netbox:\${VERSION-latest}/image: netbox_schyconf:1.0/g' ./docker-compose.yml
# sed -i 's/- 8080/- 8000:8080/g' docker-compose.yml
docker build --pull --target main -f netbox-docker/Dockerfile -t netbox_schyconf:1.0 --build-arg NETBOX_PATH=netbox-docker/.netbox --build-arg FROM=python:3.8-alpine .
docker-compose -f netbox-docker/docker-compose.yml up -d
#######




 