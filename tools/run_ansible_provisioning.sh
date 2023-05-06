#!/bin/bash

BASEDIR="$(readlink -f $0 | xargs dirname)/.."

ansible-galaxy install --force -r $BASEDIR/tools/ansible_runbook/requirements.yml
ansible-playbook $BASEDIR/tools/ansible_runbook/prepare_machine.yml --ask-become-pass --extra-vars "@$BASEDIR/tools/ansible_runbook/.playbook_overrides.yml"
