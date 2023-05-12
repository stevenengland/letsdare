#!/bin/bash

set -e

if [ "$EUID" -ne 0 ]; then
   echo "> Script must be run with elevated rights!"
   exit 1
fi

BASEDIR="$(readlink -f $0 | xargs dirname)/.."
IMAGES_DIR="$BASEDIR/tests/test_assets/disk_images"

echo "> Base Dir is:  $BASEDIR"
echo "> Image Dir is: $IMAGES_DIR"

echo "> Creating dir $IMAGES_DIR"
mkdir -p $IMAGES_DIR

function exit_on_error(){
  exit_code=$?
  if [ $exit_code -ne 0 ]; then
      >&2 echo "Last command failed with exit code ${exit_code}."
      exit $exit_code
  fi
}

function delete_image(){
  if test -f $1; then
    echo ">- Removing existing image: $1"
    exit_on_error
    rm $1
  fi
}

function detach_deleted_devices(){
  readarray -t devices_by_image_name  < <(losetup | grep "(deleted)" | cut -d' ' -f1)
  for i in "${devices_by_image_name[@]}"
  do
    echo ">- Detaching existing device: $i"
    losetup -d $i
    exit_on_error
  done
}

function detach_device(){
  #if [ $(losetup $1 > /dev/null 2>&1) ]; then
  #  echo "> Detaching existing device: $1"
  #  losetup -d $1
  #fi

  readarray -t devices_by_image_name  < <(losetup | grep $1 | cut -d' ' -f1)
  for i in "${devices_by_image_name[@]}"
  do
    echo ">- Detaching existing device: $i"
    losetup -d $i
    exit_on_error
  done
}

function delete_device(){
  #if [ $(dmsetup status $1 > /dev/null 2>&1) ]; then
  #if [ $(dmsetup ls | grep $1 | cut -d$'\t' -f1 > /dev/null) ]; then
  #  echo "> Removing existing device: $1"
  #  dmsetup message suspend $1
  #  dmsetup remove -f $1
  #else
  #  echo $?
  #fi
  readarray -t devices_by_image_name  < <(dmsetup ls | grep $1 | cut -d$'\t' -f1)
  for i in "${devices_by_image_name[@]}"
  do
    echo ">- Detaching existing device: $i"
    # dmsetup message suspend $i
    dmsetup remove -f $i
    exit_on_error
  done
}

function get_next_avail_loop_dev(){
  id=$(losetup -f)
  exit_on_error
  echo $id
}

function create_image(){
  image=$1
  image_size=$2
  echo ">+ Creating image: $image"
  dd if=/dev/zero of=$image bs=1M count=$image_size
  exit_on_error
}

function create_loop_device(){
  loop_device=$1
  image_filename=$2
  echo ">+ Creating loop device: $loop_device"
  losetup $loop_device $image_filename
  exit_on_error
}

function setup_block_device(){
  image=$1
  image_filename="$image.img"
  image_size=$2
  loop_device=$3

  # teardown
  delete_device $image
  detach_device $image
  delete_image $IMAGES_DIR/$image_filename

  # setup
  create_image $IMAGES_DIR/$image_filename $image_size
  create_loop_device $loop_device $IMAGES_DIR/$image_filename
}

detach_deleted_devices

################
# IMAGE CREATION SECTION
###############

# Image with corrupted MBR (completely missing)
#IMAGE="uc0005"
#LOOP_DEVICE=$(get_next_avail_loop_dev)
#setup_block_device $IMAGE 5 $LOOP_DEVICE
#
#echo "> Partitioning loop device $LOOP_DEVICE"
#parted --script $LOOP_DEVICE \
#  mktable msdos \
#  mkpart primary 1MiB 2MiB \
#  mkpart primary 2MiB 100% \
#  align-check optimal 1 \
#  align-check optimal 2 \
#  name 1 UEFI \
#  name 2 SYSTEM
#
#dd if=/dev/zero of=$LOOP_DEVICE bs=512 count=1 conv=notrunc

# Image with corrupted GPT (completely missing)
# https://serverfault.com/a/787210
IMAGE="uc0004"
LOOP_DEVICE=$(get_next_avail_loop_dev)
setup_block_device $IMAGE 5 $LOOP_DEVICE

echo "> Partitioning loop device $LOOP_DEVICE"
parted --script $LOOP_DEVICE \
  mktable gpt \
  mkpart primary 1MiB 2MiB \
  mkpart primary 2MiB 100% \
  align-check optimal 1 \
  align-check optimal 2 \
  name 1 MSDOS \
  name 2 SYSTEM

dd if=/dev/zero of=$LOOP_DEVICE bs=512 count=34 conv=notrunc

# Image with corrupted GPT (partly missing)
IMAGE="uc0003"
LOOP_DEVICE=$(get_next_avail_loop_dev)
setup_block_device $IMAGE 5 $LOOP_DEVICE

echo "> Partitioning loop device $LOOP_DEVICE"
parted --script $LOOP_DEVICE \
  mktable gpt \
  mkpart primary 1MiB 2MiB \
  mkpart primary 2MiB 100% \
  align-check optimal 1 \
  align-check optimal 2 \
  name 1 UEFI \
  name 2 SYSTEM

dd if=/dev/zero of=$LOOP_DEVICE bs=512 count=1 conv=notrunc

# Image with unreadable sectors
IMAGE="uc0002"
LOOP_DEVICE=$(get_next_avail_loop_dev)
setup_block_device $IMAGE 5 $LOOP_DEVICE

echo "> Mapping device to $LOOP_DEVICE"
dmsetup create $IMAGE << EOF
  0 8       linear $LOOP_DEVICE 0
  8 1       error
  9 1       linear $LOOP_DEVICE 9
EOF

# EFI GPT image with two partitions
IMAGE="uc0001"
LOOP_DEVICE=$(get_next_avail_loop_dev)
setup_block_device $IMAGE 5 $LOOP_DEVICE

echo "> Partitioning loop device $LOOP_DEVICE"
parted --script $LOOP_DEVICE \
  mktable gpt \
  mkpart primary 1MiB 2MiB \
  mkpart primary 2MiB 100% \
  align-check optimal 1 \
  align-check optimal 2 \
  name 1 UEFI \
  name 2 SYSTEM
  #mkpart primary fat32 2048s 4096s \
  #mkpart primary fat32 4097s 100% \

