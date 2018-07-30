# wazo-ansible

## Prerequisites for Nestbox

* You need root access on `mirror.wazo.community`.
* You need a Debian Stretch vanilla, reachable under the name `nestbox-dev-ansible` (via `/etc/hosts` for example).
* You can SSH easily into this machine.

## How to install Nestbox

* Install Ansible: `pip install ansible`
* Run `ansible-playbook -i dev mirror_keys.yml --extra-vars nestbox_mirror_user=test`
* Run `ansible-playbook -i dev nestbox.yml`
* Ensure your database server is running, if on another machine
* Run `ansible-playbook -i dev nestbox-init.yml`
* Nestbox will be installed on `nestbox-dev-ansible`

## File hierarchy

The hierarchy follows the best practices described here:

https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#directory-layout
