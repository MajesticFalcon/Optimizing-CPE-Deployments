# Phase 8: Create the Netbox webhook

When our custom script saves the new device to the database, we can configure Netbox to fire an API request. This API request will inform Ansible there is a new device that needs to have its configuration generated.


![Webhook Creation](/img/phase_8_webhook_creation.PNG)


The URL that needs to be configured will depend on your endpoint. In this scenario, I have flask running on port 5008, so my endpoint is http://server-ip:5008/create_configuration

You can leave the rest of the webhook alone, the default configuration will send all information regarding the event.

To test your new webhook, run the flask server in one window, and create a new device in Netbox. You should see an event hit the webserver and the playbook should kick off.

![Ansible Example](/img/phase_8_example.png)


