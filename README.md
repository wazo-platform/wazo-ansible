# wazo-ansible

## Prerequisites for all recipes

* Enough machines running with Debian Stretch vanilla
* You can SSH easily into those machines (i.e. without password prompt)
* Ansible: `pip install ansible`


## UC Engine (all in one machine)

* Edit `inventories/uc-engine` and set your host in `[uc-engine-host]`
* Run:

```shell
ansible-galaxy install -r requirements-postgresql.yml
ansible-galaxy install -r requirements-reverse-proxy.yml

ansible-playbook -i inventories/uc-engine uc-engine.yml
```

## Distributed Wazo

* Edit or copy `inventories/distributed` and replace the hosts `*-ansible` with your hosts
* Run:

```shell
ansible-galaxy install -r requirements-postgresql.yml
ansible-galaxy install -r requirements-reverse-proxy.yml
ansible-galaxy install -r requirements-sbc.yml

ansible-playbook -i inventories/distributed \
   postgresql.yml \
   b2bua.yml \
   engine-api.yml \
   engine-api-init.yml \
   nestbox.yml \
   nestbox-init.yml \
   router.yml \
   router-init.yml \
   edge-proxy.yml \
   reverse-proxy.yml \
   rtpengine.yml \
   sbc.yml
```
