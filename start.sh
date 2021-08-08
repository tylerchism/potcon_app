#!/usr/bin/env bash

local_workspace="$HOME/workspace"
input_dir="${local_workspace}/tmp"
output_dir="${local_workspace}/out"

if [ $(uname) == 'Linux' ]; then echo "opening app in chrome browser"; google-chrome  http://localhost:1234/examples/potcon.html; 
else open -a "Google Chrome"  http://localhost:1234/examples/potcon.html;
fi

while getopts ":i:o:" opt; do
           case $opt in
                i) input_dir=$OPTARG ;;
                o) output_dir=$OPTARG ;;
                *) echo "[-i] <folder/with/plys> [-o] <folder/with/potree/data>";;
          esac
  done
  shift $(( OPTIND - 1 ));
  
docker run --name potree_converter -it -v \
${input_dir}:/workspace/tmp -v \
${output_dir}:/opt/potree/pointclouds --rm \
-p 1234:1234 potcon