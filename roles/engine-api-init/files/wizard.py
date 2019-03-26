#!/usr/bin/python3
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse

from xivo_confd_client import Client as Confd


def init_uc_engine(language, password, engine_api_port):
    c = Confd('localhost', port=engine_api_port, https=True, prefix='/api/confd', verify_certificate='/usr/share/xivo-certs/server.crt')

    if c.wizard.get()['configured'] is not True:
        discover = c.wizard.discover()
    else:
        raise Exception("Wizard already configured...")

    wizard = {
      "admin_password": password,
      "license": True,
      "timezone": discover['timezone'],
      "language": language,
      "network": {
        "hostname": discover['hostname'],
        "domain": discover['domain'],
        "interface": discover['interfaces'][0]['interface'],
        "ip_address": discover['interfaces'][0]['ip_address'],
        "netmask": discover['interfaces'][0]['netmask'],
        "gateway": discover['gateways'][0]['gateway'],
        "nameservers": discover['nameservers']
      },
      "steps": {
         "manage_services": False,
         "manage_hosts_file": False,
         "manage_resolv_file": False,
         "commonconf": False,
      }
    }

    return c.wizard.create(wizard)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', action='store')
    parser.add_argument('--password', action='store')
    parser.add_argument('--no-fail', action='store_true')
    parser.add_argument('--engine-api-port', action='store')
    return parser.parse_args()


def main():
    args = _parse_args()
    try:
        init_uc_engine(args.language, args.password, args.engine_api_port)
    except Exception:
        if not args.no_fail:
            raise


if __name__ == '__main__':
    main()
