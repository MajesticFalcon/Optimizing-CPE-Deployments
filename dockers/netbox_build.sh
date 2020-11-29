!#/usr/bin/bash
git clone https://github.com/netbox-community/netbox-docker.git
git clone https://github.com/netbox-community/netbox.git netbox-docker/.netbox
cd ./netbox-docker
sed -i "35i RUN echo \"py-zabbix\" >> /requirements.txt" Dockerfile
sed -i 's/image: netboxcommunity\/netbox:\${VERSION-latest}/image: netbox_schyconf:1.0/g' ./docker-compose.yml
sed -i 's/- 8080/- 8000:8080/g' docker-compose.yml
docker build --pull --target main -f Dockerfile -t netbox_schyconf:1.0 --build-arg NETBOX_PATH=.netbox --build-arg FROM=python:3.8-alpine .
docker-compose up -d
