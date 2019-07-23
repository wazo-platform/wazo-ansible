#!/usr/bin/env python

# Copyright: (c) 2019, Wazo Communication Inc
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from wazo_confd_client import Client as Confd


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: wazo_wizard

short_description: initial configuration of a Wazo engine

version_added: "2.4"

description:
    - "The wazo_wizard module configures a Wazo engine after a fresh installation, in order to tailor it to its new environment (password, locale, network, etc.)"

options:
    hostname:
        description:
            - This is the hostname of the Wazo engine host
        required: false
        default: localhost
    language:
        description:
            - language to use (e.g. en_US).
        required: true
    password:
        description:
            - password for the root user of the Wazo engine
        required: true
    engine_api_port:
        description:
            - password for the Wazo engine
        required: false
        default: 443
    https:
        description:
            - use https to connect to the Wazo engine
        required: false
        default:true
    prefix:
        description:
            - prefix to contact the configuration service
        required: false
        default: /api/confd
    verify_certificate:
        description:
            - verify SSL certificates
        required: false
        default: true
    provisioning_step:
        description:
            - enable the provisioning step
        required: false
        default: true
    manage_services_step:
        description:
            - enable the manage service step
        required: false
        default: true
    manage_hosts_file_step:
        description:
            - enable the manage hosts file step
        required: false
        default: true
    manage_resolv_file_step:
        description:
            - enable the manage resolv file step
        required: false
        default: true
    commonconf_step:
        description:
            - enable the commonconf step
        required: false
        default: true

author:
    - Wazo (@wazocommunity)
'''

EXAMPLES = '''
# Configure a Wazo engine
- name: Test with a message
  wazo_wizard:
    language: en_US
    password: solidpass
'''

RETURN = '''
:
    description: 
    type: str
    returned: always
'''


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        hostname=dict(type='str', required=False, default="localhost"),
        language=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        engine_api_port=dict(type='int', required=False, default=443),
        https=dict(type='bool', required=False, default=True),
        prefix=dict(type='str', required=False, default='/api/confd'),
        verify_certificate=dict(type='str', required=False, default=None),
        provisioning_step=dict(type='bool', required=False, default=True),
        manage_services_step=dict(type='bool', required=False, default=True),
        manage_hosts_file_step=dict(type='bool', required=False, default=True),
        manage_resolv_file_step=dict(type='bool', required=False, default=True),
        commonconf_step=dict(type='bool', required=False, default=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    c = Confd(module.params['hostname'],
              port=module.params['engine_api_port'],
              https=module.params['https'],
              prefix=module.params['prefix'],
              verify_certificate=module.params['verify_certificate'])

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    result['changed'] = c.wizard.get()['configured'] is not True

    if result['changed']:
        discover = c.wizard.discover()

        wizard = {
            "admin_password": module.params['password'],
            "license": True,
            "timezone": discover['timezone'],
            "language": module.params['language'],
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
                "provisioning": module.params['provisioning_step'],
                "manage_services": module.params['manage_services_step'],
                "manage_hosts_file": module.params['manage_hosts_file_step'],
                "manage_resolv_file": module.params['manage_resolv_file_step'],
                "commonconf": module.params['commonconf_step'],
            }
        }

        c.wizard.create(wizard)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

# wazo.py ends here
