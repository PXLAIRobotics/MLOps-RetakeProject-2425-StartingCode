#!/bin/bash
set -eux

# Default values
USERNAME=${USERNAME:-user}
USER_UID=${USER_UID:-1001}
USER_GID=${USER_GID:-1001}
USER_PASSWORD=${USER_PASSWORD:-changeme}

# Check if group exists by GID
if getent group "$USER_GID" > /dev/null; then
    GROUPNAME=$(getent group "$USER_GID" | cut -d: -f1)
else
    GROUPNAME="$USERNAME"
    groupadd -g "$USER_GID" "$GROUPNAME"
fi

# Check if user exists by UID
if getent passwd "$USER_UID" > /dev/null; then
    # Reuse existing user
    USERNAME=$(getent passwd "$USER_UID" | cut -d: -f1)
else
    # Ensure username is unique if we're about to create it
    BASE_NAME="$USERNAME"
    i=1
    while id "$USERNAME" >/dev/null 2>&1; do
        USERNAME="${BASE_NAME}_alt${i}"
        i=$((i + 1))
    done

    # Create the user with specified UID/GID
    useradd -m -u "$USER_UID" -g "$USER_GID" -s /bin/bash "$USERNAME"
    echo "$USERNAME:$USER_PASSWORD" | chpasswd
fi

# Always ensure sudo access (even for reused users)
echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/$USERNAME"
chmod 0440 "/etc/sudoers.d/$USERNAME"

# Save values for Dockerfile layers to use
echo "USERNAME=$USERNAME" > /env_vars
echo "GROUPNAME=$GROUPNAME" >> /env_vars

# Optional debug output
echo "INFO: USERNAME = $USERNAME"
echo "INFO: GROUPNAME = $GROUPNAME"
