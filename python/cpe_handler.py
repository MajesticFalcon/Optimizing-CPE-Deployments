import asyncio
from pythonping import ping
import os

async def work():
    detected_device = False
    detection_counter = 0
    while True:
        await asyncio.sleep(1)
        if(ping('192.168.255.3')):
            print("tru")
            detection_counter += 1
        else:
            print("fal")
        if detection_counter > 10:
            print("found a device")
            os.system("ansible-playbook \
              -i /optimizing_cpes/ansible/netbox_inventory.yml \
              /optimizing_cpes/ansible/sftp_test.yml")
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