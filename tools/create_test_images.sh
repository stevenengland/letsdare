#!/bin/bash

set -e

BASEDIR="$(readlink -f $0 | xargs dirname)/.."
IMAGES_DIR="$BASEDIR/tests/test_assets/disk_images"

echo "$BASEDIR"
echo "$IMAGES_DIR"

mkdir -p $IMAGES_DIR

# EFI GPT image with two partitions
if test -f $IMAGES_DIR/uc0001.img; then
    rm $IMAGES_DIR/uc0001.img
fi

dd if=/dev/zero of=$IMAGES_DIR/uc0001.img bs=1M count=5

parted --script $IMAGES_DIR/uc0001.img \
  mktable gpt \
  mkpart primary 1MiB 2MiB \
  mkpart primary 2MiB 100% \
  align-check optimal 1 \
  align-check optimal 2 \
  name 1 UEFI \
  name 2 SYSTEM
  #mkpart primary fat32 2048s 4096s \
  #mkpart primary fat32 4097s 100% \
