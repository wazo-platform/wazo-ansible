#!/bin/bash

set -e

confd_db_host="$1"
confd_db_port="$2"
confd_db_username="$3"
confd_db_password="$4"
confd_db_name="$5"
root_user="$6"
root_password="$7"

# Add certificate in auth section:
cat > ~/.config/wazo-auth-cli/50-certificate.yml <<EOF
auth:
    verify_certificate: /etc/nestbox/https/public-certificate.pem
EOF

# Set wazo-auth-cli config
export WAZO_AUTH_CLI_CONFIG=~/.config/wazo-auth-cli
cat > ~/.bashrc <<EOF
export WAZO_AUTH_CLI_CONFIG=~/.config/wazo-auth-cli
EOF

# Create your super user policy
NESTBOX_POLICY=$(wazo-auth-cli policy create --description "Default super user nestbox policy" --acl "auth.#" "deployd.#" "confd.#" -- nestbox_default_super_user)

# Create your super user
NESTBOX_TENANT=$(wazo-auth-cli tenant create admin-tenant)
NESTBOX_USER=$(wazo-auth-cli user create --firstname John --lastname Doe --password "$root_password" --email "john@example.com" --tenant "$NESTBOX_TENANT" "$root_user")
wazo-auth-cli user add --policy "$NESTBOX_POLICY" "$NESTBOX_USER"

# Add the cli policy to the cli user
NESTBOX_CLI_POLICY=$(wazo-auth-cli policy create --description "wazo-auth-cli policy" --acl "auth.#" -- wazo_auth_cli_policy)
wazo-auth-cli user add --policy "$NESTBOX_CLI_POLICY" wazo-auth-cli

# Clean Wazo default policy
wazo-auth-cli policy delete wazo_default_user_policy
wazo-auth-cli policy delete wazo_default_admin_policy
wazo-auth-cli policy delete wazo_default_master_user_policy

# Create defaults policies for Reseller/Customer/Location
NESTBOX_RESELLER_POLICY=$(wazo-auth-cli policy create --description "Default reseller nestbox policy" --acl "auth.users.#" "auth.tenants.#" "auth.groups.#" "auth.policies.#" "deployd.#" "confd.#" -- nestbox_default_reseller)
NESTBOX_CUSTOMER_POLICY=$(wazo-auth-cli policy create --description "Default customer nestbox policy" --acl "auth.users.me.#" "deployd.instances.*.credentials.#.read" "confd.#" -- nestbox_default_customer)
NESTBOX_LOCATION_POLICY=$(wazo-auth-cli policy create --description "Default location nestbox policy" --acl "auth.users.me.#" "deployd.instances.*.credentials.#.read" "confd.#" -- nestbox_default_location)

# Create nestbox-ui config
mkdir -p /etc/nestbox-ui/conf.d
cat >/etc/nestbox-ui/conf.d/50-default-policies.yml <<EOL
policies:
    reseller: ${NESTBOX_RESELLER_POLICY}
    customer: ${NESTBOX_CUSTOMER_POLICY}
    location: ${NESTBOX_LOCATION_POLICY}
EOL

# Create nestbox-confd reseller
psql "postgresql://$confd_db_username:$confd_db_password@$confd_db_host:$confd_db_port/$confd_db_name" -c "INSERT INTO confd_reseller values ('$NESTBOX_TENANT', 'admin-reseller', now() at time zone 'utc');"
