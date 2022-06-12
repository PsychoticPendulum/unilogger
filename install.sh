#! /bin/bash

THIS_VERSION=$(./PyTerm.py --version)
INST_VERSION=$(/home/$USER/.local/lib/python3.10/site-packages/PyTerm.py --version)

if [[ $THIS_VERSION = $INST_VERSION ]]; then
    echo "$THIS_VERSION is already installed"
    exit
fi

log INFO "Installing PyTerm module for $USER"
cp -Rfv *.py ~/.local/lib/python3.10/site-packages/
