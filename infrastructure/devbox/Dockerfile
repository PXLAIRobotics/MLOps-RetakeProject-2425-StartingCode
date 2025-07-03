FROM ubuntu:24.04

USER root

# We love UTF!
ENV LANG=C.UTF-8

### Envrionment config 
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Set the nvidia container runtime
ARG NVIDIA_VISIBLE_DEVICES=all
ARG NVIDIA_DRIVER_CAPABILITIES=graphics
ENV NVIDIA_VISIBLE_DEVICES=${NVIDIA_VISIBLE_DEVICES}
ENV NVIDIA_DRIVER_CAPABILITIES=${NVIDIA_DRIVER_CAPABILITIES}

# Updated and add sudo
RUN apt-get update \
	&& apt-get --with-new-pkgs upgrade -y \
    && apt-get install -y sudo 

# Clean up motd stuff
RUN rm -f /etc/update-motd.d/10-help-text

# Add the user-creation script
COPY ./create_user.bash /usr/local/bin/
RUN chmod +x /usr/local/bin/create_user.bash

# Create user and persist final values
# Accept the needed build arguments.
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000
ARG USER_PASSWORD=changeme

# Pass ARGs into ENV so they are visible to the script
ENV USERNAME=${USERNAME} \
    USER_UID=${USER_UID} \
    USER_GID=${USER_GID} \
    USER_PASSWORD=${USER_PASSWORD}
RUN  /usr/local/bin/create_user.bash
RUN unset USER_PASSWORD

#  Pre-Made Virtualenv
RUN set -a && . /env_vars && set +a && \
    apt-get install -y --no-install-recommends python3 python3-venv && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools && \
    chown -R "$USERNAME:$GROUPNAME" /opt/venv && \
    echo 'export PATH="/opt/venv/bin:$PATH"' >> /home/$USERNAME/.bashrc

# Copy requirements.txt into the image
COPY requirements.txt /opt/requirements.txt

# Install Python packages using pip inside the venv
RUN set -a && . /env_vars && set +a && \
    /opt/venv/bin/pip install --no-cache-dir -r /opt/requirements.txt && \
    chown -R $USERNAME:$GROUPNAME /opt/venv

# Install other tools including git, tmux, htop, vim, gosu, ...
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git tmux htop vim gosu && \
    rm -rf /var/lib/apt/lists/*

# Tmux setup
RUN set -a && . /env_vars && set +a && \
    mkdir -p /home/$USERNAME/.tmux/plugins/tpm && \
    git clone https://github.com/tmux-plugins/tpm /home/$USERNAME/.tmux/plugins/tpm && \
    git clone https://github.com/jimeh/tmux-themepack.git /home/$USERNAME/.tmux-themepack

# Set PS1 to something simple
RUN set -a && . /env_vars && set +a && \
    echo "PS1='${debian_chroot:+(\$debian_chroot)}\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\W\\[\\033[00m\\]\\$ '" >> /home/$USERNAME/.bashrc

# Copy tmux config
COPY .tmux.conf /tmp/.tmux.conf
RUN set -a && . /env_vars && set +a && \
    cp /tmp/.tmux.conf /home/$USERNAME/.tmux.conf && \
    chown $USERNAME:$GROUPNAME /home/$USERNAME/.tmux.conf


# Bash profile and aliases
RUN set -a && . /env_vars && set +a && \
    mkdir /data /commands /scripts /home/$USERNAME/bin && \
    echo 'source "$HOME/.bashrc"' >> /home/$USERNAME/.bash_profile && \
    echo "alias ll='ls --color=auto -alFh'" >> /home/$USERNAME/.bashrc && \
    echo "LS_COLORS=\$LS_COLORS:'di=1;33:ln=36'" >> /home/$USERNAME/.bashrc && \
    echo 'export LS_COLORS' >> /home/$USERNAME/.bashrc && \
    echo 'alias tmux="tmux -2"' >> /home/$USERNAME/.bashrc && \
    echo 'PATH=~/bin:/commands:/scripts/:$PATH' >> /home/$USERNAME/.bashrc

# Make sure these match your actual user from /env_vars
RUN set -a && . /env_vars && set +a

COPY ./entrypoint.bash /usr/local/bin/dev_entry
RUN chmod +x /usr/local/bin/dev_entry

ENTRYPOINT ["/usr/local/bin/dev_entry"]
CMD ["bash", "-l"]
