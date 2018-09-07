# wazo-ansible

## Prerequisites for all recipes

* A machine running with Debian Stretch vanilla
* You can SSH easily into this machine
* Install Ansible: `pip install ansible`

## Prerequisites

* You need a valid certificate to access the package repository.
  * If you have root access on mirror.wazo.io, you can get them with:
    `ansible-playbook -i dev mirror_keys.yml --extra-vars nestbox_mirror_user=test`

## Recipes

### B2BUA

* Run `ansible-playbook -i dev b2bua.yml`
* The B2BUA will be installed on `b2bua-ansible`

### Edge proxy

* Run `ansible-playbook -i dev edge-proxy.yml`
* The edge proxy will be installed on `edge-proxy-ansible`

### Engine API

* Run `ansible-playbook -i dev engine-api.yml`
* Ensure your database server is running, if on another machine
* Run `ansible-playbook -i dev engine-api-init.yml`
* The engine API will be installed on `engine-api-ansible`

### Nestbox

* Run `ansible-playbook -i dev nestbox.yml`
* Ensure your database server is running, if on another machine
* Run `ansible-playbook -i dev nestbox-init.yml`
* Nestbox will be installed on `nestbox-dev-ansible`, linked to `database-ansible` as its database server.

### PostgreSQL

* Run `ansible-galaxy install -r requirements-postgresql.yml`
* Run `ansible-playbook -i dev postgresql.yml`
* PostgreSQL will be installed on `postgresql-ansible`

### Reverse proxy HTTP

* Run `ansible-galaxy install -r requirements-reverse-proxy.yml`
* Run `ansible-playbook -i dev reverse-proxy.yml`
* The HTTP reverse proxy will be installed on `reverse-proxy-ansible`

### Router

* Run `ansible-playbook -i dev router.yml`
* Ensure your database server is running, if on another machine
* Run `ansible-playbook -i dev router-init.yml`
* The router will be installed on `router-ansible`

### RTP Engine

* Run `ansible-playbook -i dev rtpe.yml`
* The RTP engine will be installed on `rtpengine-ansible`

### SBC

* Run `ansible-galaxy install -r requirements-sbc.yml`
* Run `ansible-playbook -i dev sbc.yml`
* The SBC will be installed on `sbc-ansible`

## Variables

### b2bua

* `b2bua_host`: (default: `b2bua-ansible`) where other services should contact the B2BUA
* `b2bua_port_ami`: (default: `5038`) TCP port for AMI
* `b2bua_port_http`: (default: `5039`) TCP port for HTTP interfaces
* `b2bua_port_https`: (default: `5040`) TCP port for HTTPS interfaces
* `b2bua_port_sysconfd`: (default: `8668`) TCP port for xivo-sysconfd HTTP interface
* `b2bua_https_cert`: (default: `files/default-https.crt`) custom certificate for HTTPS
* `b2bua_https_private_key`: (default: `files/default-https.key`) custom private key for HTTPS
* `b2bua_wazo_distribution`: (default: `wazo-dev-stretch`) wazo distribution from where packages are installed

### database

`postgresql_port`: (default: `5432`) TCP port for PostgreSQL
`postgresql_superuser_password`: (default: `superpass`) password for superuser `postgres`

### edge-proxy

This recipe uses the role mwolff44.kamailio-mw, the complete list of variables is available [on Github](https://github.com/mwolff44/kamailio-mw#role-variables). Here are the most interesting ones:

* `kamailio_creatordb_host`
* `kamailio_db_host`
* `kamailio_db_port`
* `kamailio_db_root_user`
* `kamailio_db_root_pass`
* `kamailio_db_name`
* `kamailio_db_user`
* `kamailio_db_pass`
* `kamailio_db_user_ro`
* `kamailio_db_pass_ro`

All variable can be shared with other recipes, except `kamailio_creatordb_host` which should be applied only on the `edge-proxy` group.

### engine-api

* `engine_api_host`: (default: `engine-api-ansible`) where other services should contact the engine API
* `engine_api_port`: (default: `443`) TCP port for HTTPS API
* `engine_api_port_confgend`: (default: `8669`) TCP port for xivo-confgend
* `engine_api_https_cert`: (default: `files/default-https.crt`) custom certificate for HTTPS
* `engine_api_https_private_key`: (default: `files/default-https.key`) custom private key for HTTPS
* `engine_api_wazo_distribution`: (default: `wazo-dev-stretch`) wazo distribution from where packages are installed
* `engine_db_host`: (default: `database-ansible`) PostgreSQL host
* `engine_db_port`: (default: `5432`) PostgreSQL port
* `engine_db_admin_user`: (default: `postgres`) PostgreSQL superuser username
* `engine_db_admin_password`: (default: `superpass`) PostgreSQL superuser password
* `engine_db_auth_name`: (default: `wazo-auth`) database name for wazo-auth
* `engine_db_auth_user`: (default: `wazo-auth`) database username for wazo-auth
* `engine_db_auth_password`: (default: `superpass`) database password for wazo-auth
* `engine_db_confd_name`: (default: `asterisk`) database name for xivo-confd
* `engine_db_confd_user`: (default: `asterisk`) database username for xivo-confd
* `engine_db_confd_password`: (default: `superpass`) database password for xivo-confd
* `ari_username`: (default: `xivo`) B2BUA ARI username
* `ari_password`: (default: `Nasheow8Eag`) B2BUA ARI password
* `ami_username`: (default: `xivo_amid`) B2BUA AMI username
* `ami_password`: (default: `eeCho8ied3u`) B2BUA AMI password
* `entity_name`: (default: `Wazo`) first entity name
* `language`: (default: `en_US`)
* `number_start`: (default: `1000`) start of phone numbers range
* `number_end`: (default: `1999`) end of phone numbers range
* `engine_root_password`: (default: `superpass`) password for engine superuser `root`
* `postgresql_pinned_version`: (default: `9.6.10-0+deb9u1`) version of package postgresql-9.1

### mirror keys

* `nestbox_mirror_user`: (no default value) the name of the certificate that will be created on the mirror to access the private Debian repo

### private mirror access

* `nestbox_repo_client_cert`: (no default value) certificate used to access the private package repository
* `nestbox_repo_client_key`: (no default value) private key used to access the private package repository

### nestbox

Variables that control the path for certificates used for HTTPS:

* `nestbox_host`: (default: `nestbox-ansible`) where other services should contact Nestbox
* `nestbox_port`: (default: `443`) TCP port for HTTPS
* `nestbox_db_host`: (default: `database-ansible`) PostgreSQL host
* `nestbox_db_port`: (default: `5432`) PostgreSQL port
* `nestbox_db_admin_user`: (default: `postgres`) PostgreSQL superuser username
* `nestbox_db_admin_password`: (default: `superpass`) PostgreSQL superuser password
* `nestbox_db_auth_name`: (default: `nestbox-auth`) database name for wazo-auth
* `nestbox_db_auth_user`: (default: `wazo-auth`) database username for wazo-auth
* `nestbox_db_auth_password`: (default: `superpass`) database password for wazo-auth
* `nestbox_db_confd_name`: (default: `nestbox-confd`) database name for nestbox-confd
* `nestbox_db_confd_user`: (default: `nestbox-confd`) database username for nestbox-confd
* `nestbox_db_confd_password`: (default: `superpass`) database password for nestbox-confd
* `nestbox_db_deployd_name`: (default: `wazo-deployd`) database name for wazo-deployd
* `nestbox_db_deployd_user`: (default: `wazo-deployd`) database username for wazo-deployd
* `nestbox_db_deployd_password`: (default: `superpass`) database password for wazo-deployd
* `nestbox_https_cert`: (default: `files/default-https.crt`) custom certificate for HTTPS
* `nestbox_https_private_key`: (default: `files/default-https.key`) custom private key for HTTPS
* `nestbox_root_user`: (default: `root`) nestbox superuser username
* `nestbox_root_password`: (default: `secret`) nestbox superuser password
* `postgresql_pinned_version`: (default: `9.6.10-0+deb9u1`) version of package postgresql-9.1

### reverse-proxy

* `reverse_proxy_engine_api`: (default: `true`) should engine APIs be exposed by reverse-proxy?
* `reverse_proxy_https_cert`: (default: `files/default-https.crt`) custom certificate for HTTPS
* `reverse_proxy_https_private_key`: (default: `files/default-https.key`) custom private key for HTTPS

### router

* `router_host`: (default: `router-ansible`) where other services should contact the router
* `router_port`: (default: `443`) TCP port for HTTPS API
* `router_db_host`: (default: `localhost`) PostgreSQL host
* `router_db_port`: (default: `5432`) PostgreSQL port
* `router_db_admin_user`: (default: `postgres`) PostgreSQL superuser username
* `router_db_admin_password`: (default: `superpass`) PostgreSQL superuser password
* `router_db_auth_name`: (default: `router-auth`) database name for wazo-auth
* `router_db_auth_user`: (default: `wazo-auth`) database username for wazo-auth
* `router_db_auth_password`: (default: `superpass`) database password for wazo-auth
* `router_db_confd_name`: (default: `router-confd`) database name for router-confd
* `router_db_confd_user`: (default: `router-confd`) database username for router-confd
* `router_db_confd_password`: (default: `superpass`) database password for router-confd
* `router_https_cert`: (default: `files/default-https.crt`) custom certificate for HTTPS
* `router_https_private_key`: (default: `files/default-https.key`) custom private key for HTTPS
* `router_root_user`: (default: `root`) router superuser username
* `router_root_password`: (default: `superpass`) router superuser password
* `postgresql_pinned_version`: (default: `9.6.10-0+deb9u1`) version of package postgresql-9.1

### sbc

* `sbc_host`: (default: `sbc-ansible`) where other services should contact the sbc
* `sbc_port_kamailio_http`: (default: `8888`) TCP port for HTTP RPC


## File hierarchy

The hierarchy follows the best practices described here:

https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#directory-layout
