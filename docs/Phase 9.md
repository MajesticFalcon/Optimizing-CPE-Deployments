# Phase 9: Uploading configurations to Gitlab

Ansible has the ability to work with Git, but doesn't quite have all the features we need. We can use shell here.

I am assuming the git repo has already been created and PKI setup has been completed. If not, see [this](https://docs.gitlab.com/ee/ssh/) guide.

```python
@app.route('/create_configuration', methods=['POST'])
def create_configuration():
    device_name = request.json["data"]["name"]
    os.system("ansible-playbook -i /docker/netbox_inventory.yml /docker/create_configuration.yml -e 'device_name={0}'".format(device_name))
    os.system("git -C /docker/git add .")
    os.system("git -C /docker/git commit -am 'auto commit from webhook'")
    os.system("git -C /docker/git push origin master")
    return("/")
```

