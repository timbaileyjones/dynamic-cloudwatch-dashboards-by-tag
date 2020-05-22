#!/bin/bash
set -ex
mkdir -p dist

git checkout dist/cloudwatch-dashboards-updater.zip
cd ./src && zip -r -9 ../dist/cloudwatch-dashboards-updater.zip .
#export PYTHONPATH=$PWD
cd ..  
python3 ./dist/cloudwatch-dashboards-updater.zip  $*
