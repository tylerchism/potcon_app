#!/usr/bin/env bash

r_flag=""
c_flag=""

while getopts ":rc" opt; do
           case $opt in
                r) r_flag=' -r' ;;
                c) c_flag=' -c' ;;
                *) echo "[-c] for conversion [-r] for render [-cr] to do both" ;;
          esac
  done
  shift $(( OPTIND - 1 ));

docker exec -it potree_converter python3 /home/script/runtimejob.py${r_flag}${c_flag}