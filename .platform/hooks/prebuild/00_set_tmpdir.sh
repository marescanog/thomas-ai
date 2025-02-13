#!/bin/bash
echo "Setting TMPDIR to /var/tmp"
export TMPDIR=/var/tmp
export TEMP=/var/tmp
export PIP_NO_CACHE_DIR=1
# Optionally, print the variables to verify:
echo "TMPDIR is: $TMPDIR"
echo "TEMP is: $TEMP"
