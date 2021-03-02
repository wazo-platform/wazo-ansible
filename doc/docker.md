# Docker

To have the smallest possible changes between a deployment in pure
Ansible and a container based one, Docker images are built from
ansible roles.

The `bin/role2docker` script creates the Docker image for a specific Ansible
role based on the `debian:buster-slim` image. For example: `./bin/role2docker
wazo-message-bus` will generate the Docker image named
`wazo-platform/wazo-message-bus`.

## Settings

The role that is used to create a container must have a `docker` directory.

This `docker` directory can contain the following files:

`pre`: executable to run before installing the role on the
container. This is usually used to install dependencies from galaxy.

`post`: executable run after installing the role.

`cmd`: [`CMD` instruction](https://docs.docker.com/engine/reference/builder/#cmd)
for the generated `Dockerfile`.

`init`: executable that is copied in `/init` and used as the entry
point if `cmd` is not provided.

## Labels

The list of packages is saved in the `org.wazo-platform.pkgs` label.

The `wazo_debian_repo` is saved in the
`org.wazo-platform.wazo_debian_repo` label and `wazo_distribution` in
the `org.wazo-platform.wazo_distribution` label.

## Constraints on roles

Roles should not execute any runtime commands like reloading services
when used in docker builds. To prevent this from happening, use the
`runtime` variable to protect the tasks. Example:

```
- name: reload asterisk dialplan
  command: asterisk -rx 'dialplan reload'
  when: runtime
```

Generated files like certs or tokens should be removed when not in
`runtime` mode and generated at service start. For example, the
generated files from `xivo-certs` should be removed like this:

```
- name: Remove generated files
  file:
    path: "{{ item }}"
    state: absent
  with_items:
    - /usr/share/xivo-certs/server.key
    - /usr/share/xivo-certs/server.crt
  when: not runtime
```

And the service should create them on start in its init script:

```
/var/lib/dpkg/info/xivo-certs.postinst configure
```

## Constraints on services

Services should get their settings/configuration from Consul to be able to run
in containers, in accordance with
[WPEP-2](https://github.com/wazo-platform/wpep). The only settings that should
be provided by the container management system are the environment variables to
configure Consul. See the available ones at
https://www.consul.io/docs/commands/#environment-variables.
