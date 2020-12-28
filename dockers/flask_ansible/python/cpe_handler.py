import asyncio
from pythonping import ping
from subprocess import Popen, PIPE
import pysftp
import os

async def work():
    detected_device = False
    detection_counter = 0
    while True:
        await asyncio.sleep(1)
        if(ping('192.168.88.1')):
            print("tru")
            detection_counter += 1
        else:
            print("fal")
        if detection_counter > 10:
            print("found a device")
            with pysftp.Connection('192.168.88.1', username='admin', password='') as sftp:
                sftp.put('/optimizing_cpes/gitlab/auto_config.rsc')
                sftp.put('/ansible/playbooks/models/routeros/reset_configuration.auto.rsc')

            detection_counter = 0

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(work())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()