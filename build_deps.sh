#!/bin/bash -x
#/usr/bin/env bash

BUILD_DIR=$1
TOOLS_PREFIX=$2
TYPE=$3

echo $BUILD_DIR
echo $TOOLS_PREFIX
echo $TYPE

cd $BUILD_DIR

rm -rf addons/skin.touched

cd tools/depends

./bootstrap || exit 1

./configure \
        --with-ndk=${TOOLS_PREFIX}/android-ndk-r7-crystax-5.beta3 \
        --with-sdk-path=${TOOLS_PREFIX}/android-sdk-linux \
        --with-toolchain=${TOOLS_PREFIX}/android-sdk-linux/android-9-xaf-set_top \
        --with-tarballs=${TOOLS_PREFIX}/tarballs \
        --prefix=${TOOLS_PREFIX}/prefixes/android-9-neon-xaf-set_top \
		--host=arm-linux-androideabi \
        --with-sdk=android-9 || exit 1

make -j10
make

cd ../../
