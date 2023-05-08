#!/bin/bash

BASEDIR="$(readlink -f $0 | xargs dirname)/.."
BECOME_FLAG=""

if [ "$EUID" -ne 0 ]; then
   BECOME_FLAG="--ask-become-pass"
fi

if [ -n "${PW_LESS_SUDO}" ] && [ "${PW_LESS_SUDO}" = true  ];then
  BECOME_FLAG="-b"
fi

ansible-galaxy install --force -r $BASEDIR/tools/ansible_runbook/requirements.yml

if test -f $BASEDIR/tools/ansible_runbook/.playbook_overrides.yml; then
  ansible-playbook $BASEDIR/tools/ansible_runbook/prepare_machine.yml $BECOME_FLAG --extra-vars "@$BASEDIR/tools/ansible_runbook/.playbook_overrides.yml"
else
  ansible-playbook $BASEDIR/tools/ansible_runbook/prepare_machine.yml $BECOME_FLAG
fi
