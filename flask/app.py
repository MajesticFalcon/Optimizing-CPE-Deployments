import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
from flask import Flask
from markupsafe import escape
import os
import time
from flask import request
app = Flask(__name__)


    
    
    
    

@app.route('/create_configuration', methods=['POST'])
def create_configuration():
    device_name = request.json["data"]["name"]
    os.system("ansible-playbook -i /optimizing_cpes/ansible/netbox_inventory.yml /optimizing_cpes/ansible/create_configuration.yml -e 'device_name={0}'".format(device_name))
    os.system("git -C /optimizing_cpes/gitlab add .")
    os.system("git -C /optimizing_cpes/gitlab commit -am 'auto commit from webhook'")
    os.system("git -C /optimizing_cpes/gitlab push origin master")
    return("/")
@app.route('/test_ocnos', methods=['POST'])
def test_ocnos():
    os.system("ansible-playbook -i /optimizing_cpes/ansible/netbox_inventory.yml /optimizing_cpes/ansible/ocnos_test.yml")
    return("/")
    
if __name__ == '__name__':
    app.run()

app.run(host='0.0.0.0',port=5008)

