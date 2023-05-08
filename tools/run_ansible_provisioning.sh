#!/bin/bash

BASEDIR="$(readlink -f $0 | xargs dirname)/.."
ASK_BECOME_PASS=""

if [ "$EUID" -ne 0 ]; then
   ASK_BECOME_PASS="--ask-become-pass"
fi

ansible-galaxy install --force -r $BASEDIR/tools/ansible_runbook/requirements.yml

if test -f $BASEDIR/tools/ansible_runbook/.playbook_overrides.yml; then
  ansible-playbook $BASEDIR/tools/ansible_runbook/prepare_machine.yml $ASK_BECOME_PASS --extra-vars "@$BASEDIR/tools/ansible_runbook/.playbook_overrides.yml"
else
  ansible-playbook $BASEDIR/tools/ansible_runbook/prepare_machine.yml $ASK_BECOME_PASS
fi
