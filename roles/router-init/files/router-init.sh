#!/bin/bash

https_certificate=$1

# Add certificate in auth section:
cat > ~/.config/wazo-auth-cli/50-certificate.yml <<EOF
auth:
    verify_certificate: $https_certificate
EOF

# Set wazo-auth-cli config
export WAZO_AUTH_CLI_CONFIG=~/.config/wazo-auth-cli
cat > ~/.bashrc <<EOF
export WAZO_AUTH_CLI_CONFIG=~/.config/wazo-auth-cli
EOF

# Create your super user policy
WAZO_POLICY=$(wazo-auth-cli policy create --description "Default super user nestbox policy" --acl "auth.#" "confd.#" -- wazo_default_super_user)

# Create your super user
WAZO_TENANT=$(wazo-auth-cli tenant create admin-tenant)
WAZO_USER=$(wazo-auth-cli user create --firstname John --lastname Doe --password secret --email "john@example.com" --tenant $WAZO_TENANT root)
wazo-auth-cli user add --policy $WAZO_POLICY $WAZO_USER

# Add the cli policy to the cli user
WAZO_CLI_POLICY=$(wazo-auth-cli policy create --description "wazo-auth-cli policy" --acl "auth.#" -- wazo_auth_cli_policy)
wazo-auth-cli user add --policy $WAZO_CLI_POLICY wazo-auth-cli

# Clean Wazo default policy
wazo-auth-cli policy delete wazo_default_user_policy
wazo-auth-cli policy delete wazo_default_admin_policy
wazo-auth-cli policy delete wazo_default_master_user_policy
