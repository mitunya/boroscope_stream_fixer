#!/bin/bash
# ⓒ 2019 Nathan Henrie n8henrie.com
# Use at your own risk, setting a network password or apname with illegal or
# insufficient characters may brick your device
#
# Depencendies:
#   xxd V1.10 27oct98 by Juergen Weigert
#   netcat (The GNU Netcat) 0.7.1 Copyright (C) 2002 - 2003  Giovanni Giacobbi

# add Resolution change script, Copyright(c) 2026 mit unya.
# WiFi Endscope Model:WF010/020

set -euf -o pipefail

send() {
  xxd -r -p <<<"53 45 54 43 4d 44 00 14 00 00 90 00 01 00 00" | nc -u -w1 192.168.10.123 50000
  xxd -r -p <<<"53 45 54 43 4d 44 00 00 00 00 $1" | nc -u -w1 192.168.10.123 50000 | xxd -g1
}

USAGE=$(cat <<'EOF'
Valid commands:
  Reboot
  set_apname APNAME
  clear_password
  set_password PASSWORD
  res320x240
  res640x480
  res800x600
  res1024x768
  res1280x720
EOF
)

if [ $# -eq 0 ]; then
  echo "$USAGE"
  exit 1
fi

case "$1" in
  reboot) send '04 00 00 00';;
  set_apname) send "01 00 08 00 $(xxd -p <<<"$2")";;
  clear_password) send '03 00 00 00';;
  set_password) send "02 00 08 00 $(xxd -p <<<"$2")";;
  # mjpeg
  res320x240)   send "08 00 05 00 40 01 f0 00 1e" ;;
  res640x480)   send "08 00 05 00 80 02 e0 01 1e" ;;
  res800x600)   send "08 00 05 00 20 03 58 02 1e" ;;
  res1024x768)  send "08 00 05 00 00 04 00 03 1e" ;;
  res1280x720)  send "08 00 05 00 00 05 d0 02 1e" ;;
  #
  *) echo "$USAGE";;
esac
