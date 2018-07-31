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
* Run `ansible-playbook -i dev nestbox-init.yml --extra-vars "db_host=remote db_admin_password=secret"`
* Nestbox will be installed on `nestbox-dev-ansible`

## Variables

### mirror_keys.yml

* `nestbox_mirror_user`: the username of the user who will SSH into the mirror to access the private Debian repo

### nestbox.yml

Variables that control the path for certificates used for HTTPS:

* `https_certificate`: Default: `/etc/nestbox/https/public-certificate.pem`
* `https_private_key`: Default: `/etc/nestbox/https/private-key.pem`

### nestbox-init.yml

Variables that control the database initialization:

* `db_admin_user`: Default: `postgres`
* `db_admin_password`: Default: `superpass`

* `db_confd_user`: Default: `nestbox-confd`
* `db_confd_password`: Default: `superpass`

* `db_deployd_user`: Default: `wazo-deployd`
* `db_deployd_password`: Default: `superpass`

* `db_host`: Default: `localhost`

## File hierarchy

The hierarchy follows the best practices described here:

https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#directory-layout
