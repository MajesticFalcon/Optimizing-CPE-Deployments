# Phase 4: Creating an endpoint for the webhooks

More complex networks typically have some sort of webserver or automation already in place. If you have a solution similar to Salt Stack, skip this skection.

Netbox provides a method for firing web requests when certain actions happen. The intricaticies of Netbox's webhooks is beyond this primer. 

To put it simply, you can fire on the typical 3 events: create, update, delete for devices and other things tracked in Netbox. For a full list, check out their [webhook](https://netbox.readthedocs.io/en/stable/additional-features/webhooks/) documentation.

In the next phase, we will configure the webhook, but first, we need an endpoint to receive that webhook. We will use Flask.

```python
@app.route('/create_configuration', methods=['POST'])
def create_configuration():
    device_name = request.json["data"]["name"]
    os.system("ansible-playbook -i /docker/netbox_inventory.yml /docker/test.yml -e 'device_name={0}'".format(device_name))
    os.system("git -C /docker/git add .")
    os.system("git -C /docker/git commit -am 'auto commit from webhook'")
    os.system("git -C /docker/git push origin master")
    return("/")
```
