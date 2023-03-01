# wazo-ansible

## Prerequisites for all recipes

* Enough machines running with Debian Buster vanilla
* You can become root on the target machines (See https://docs.ansible.com/ansible/latest/user_guide/become.html)
* Ansible 2.7.9: `pip install ansible==2.7.9`

## UC Engine (all in one machine)

* Edit `inventories/uc-engine` and set your host in `[uc_engine_host]`
* Run:

```shell
ansible-galaxy install -r requirements-postgresql.yml

ansible-playbook -i inventories/uc-engine uc-engine.yml
```

## Variables

* `wazo_locale` if defined, ensure the locale is set and
  generated. Must be an `UTF-8` locale.

### uc_engine

* `debian_upgrade_first`: (default: `true`) do we `apt-get dist-upgrade` before installing Wazo?

### b2bua

* `b2bua_host`: (default: `localhost`) where other services should contact the B2BUA
* `b2bua_listen_address`: (default: `127.0.0.1`)
* `b2bua_port_ami`: (default: `5038`) TCP port for AMI
* `b2bua_port_http`: (default: `5039`) TCP port for HTTP interfaces
* `b2bua_port_sysconfd`: (default: `8668`) TCP port for wazo-sysconfd HTTP interface
* `b2bua_https_cert`: custom certificate filename for HTTPS
* `b2bua_https_private_key`: custom private key filename for HTTPS
* `b2bua_ami_permit_client_address`: (default: `127.0.0.1`)
* `b2bua_ami_permit_client_mask`: (default: `255.255.255.255`)
* `b2bua_listen_address`: (default: `127.0.0.1`)

### database

* `postgresql_port`: (default: `5432`) TCP port for PostgreSQL
* `postgresql_superuser_password`: password for superuser `postgres`
* `postgresql_listen_addresses`: (default: `127.0.0.1`)

### engine_api

* `engine_api_host`: (default: `localhost`) where other services should contact the engine API
* `engine_api_port`: (default: `443`) TCP port for HTTPS API
* `engine_api_port_confgend`: (default: `8669`) TCP port for wazo-confgend
* `engine_api_https_cert`: custom certificate filename for HTTPS
* `engine_api_https_private_key`: custom private key filename for HTTPS
* `engine_api_db_host`: (default: `localhost`) PostgreSQL host
* `engine_api_db_port`: (default: `5432`) PostgreSQL port
* `engine_api_db_admin_user`: (default: `postgres`) PostgreSQL superuser username
* `engine_api_db_admin_password`: PostgreSQL superuser password
* `engine_api_db_auth_name`: (default: `asterisk`) database name for wazo-auth
* `engine_api_db_auth_user`: (default: `asterisk`) database username for wazo-auth
* `engine_api_db_auth_password`: (default: `proformatique`) database password for wazo-auth
* `engine_api_db_confd_name`: (default: `asterisk`) database name for wazo-confd
* `engine_api_db_confd_user`: (default: `asterisk`) database username for wazo-confd
* `engine_api_db_confd_password`: (default: `proformatique`) database password for wazo-confd
* `engine_auth_path`: (default: `/api/auth/0.1`)
* `engine_confd_path`: (default: `/api/confd/1.1`)
* `engine_setupd_path`: (default: `/api/setupd/1.0`)
* `engine_api_listen_address`: (default: `127.0.0.1`)
* `ari_username`: (default: `xivo`) B2BUA ARI username
* `ari_password`: (default: `Nasheow8Eag`) B2BUA ARI password
* `ami_username`: (default: `wazo_amid`) B2BUA AMI username
* `ami_password`: (default: `eeCho8ied3u`) B2BUA AMI password
* `engine_api_configure_wizard`: (default: `false`) run the configuration wizard. When `true`, `engine_api_root_password` must be set.
* `api_client_name`: (default: `api-client`) client name to manage the api. Used when `engine_api_configure_wizard` is `true`.
* `api_client_password`: (default: `api-password`) password for `api_client_name`. Used when `engine_api_configure_wizard` is `true`.
* `engine_api_root_password`: password for engine superuser `root`. Used when `engine_api_configure_wizard` is `true`.
* `engine_language`: (default: `en_US`). Used when `engine_api_configure_wizard` is `true`.
* `tenant_name`: (default: `my-company`) first tenant to create. Used when `engine_api_configure_wizard` is `true`.

### debian repo and distribution

Wazo has two difference Debian repositories: the `main` and `archive`
repositories. Each repository contains multiple distributions, themselves
containing multiple packages, in a certain version:

  * The `main` repository contains the "rolling" distributions: `phoenix-buster`,
    `pelican-buster`, `wazo-dev-buster`, etc. Packages in those distributions
    are updated at each release, except `wazo-dev-buster` which is constantly
    updated.
  * The `archive` repository contains the "frozen" distributions: `wazo-19.10`,
    `wazo-19.11`, etc. Packages in those distribution do not change (except for
    important bugfixes), each distribution is created once a new version of the
    Wazo engine is released, then the packages are never updated. This ensures
    the installation will be the same, even a few months later (except for
    changes in the base Debian install).

For a new Wazo engine installation, there are two distributions to consider:

1. which distribution is used for the current installation (defined by the repo
   and distribution `wazo_debian_repo` and `wazo_distribution`)
2. which distribution will be used for future upgrades (defined by the repo and
   distribution `wazo_debian_repo_upgrade` and `wazo_distribution_upgrade`)

* `wazo_debian_repo`: (default: `main`) wazo repository from where packages are
  installed. Valid values: `main` and `archive`
* `wazo_distribution`: (default: `wazo-dev-buster`) wazo distribution from
  where packages are installed
* `wazo_debian_repo_upgrade`: (default: `main`) wazo repository for later
  upgrades. This repo is not used during installation, only set up at the end
  for later upgrades. Valid values: `main` and `archive`
* `wazo_distribution_upgrade`: (default: `wazo-dev-buster`) wazo distribution
  for later upgrades. This distribution is not used during installation, only
  set up at the end for later upgrades.
* `wazo_meta_package`: (default `wazo-platform`) meta package to
  install an all in one setup.
* `debian_repo_wazo__key_url`: URL for the package verification key
* `debian_repo_wazo__key_id`: ID of the package verification key
* `debian_repo_wazo__custom_repo`: debian repository to replace the default Wazo repository
* `debian_repo_wazo__custom_repo_filename`: filename for the debian repository to replace the default Wazo repository
* `debian_repo_wazo__custom_repo_upgrade`: debian repository to replace the custom repository for later upgrades
