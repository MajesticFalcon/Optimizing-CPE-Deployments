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
    os.system("ansible-playbook -i /docker/netbox_inventory.yml /docker/create_configuration.yml -e 'device_name={0}'".format(device_name))
    os.system("git -C /docker/git add .")
    os.system("git -C /docker/git commit -am 'auto commit from webhook'")
    os.system("git -C /docker/git push origin master")
    return("/")
    
if __name__ == '__name__':
    app.run()

app.run(host='0.0.0.0',port=5008)

