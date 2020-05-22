#!/bin/bash
set -ex
mkdir -p dist
#cd ./src && zip -r -9 ../dist/cloudwatch-dashboards-updater.zip .
git checkout ./dist/cloudwatch-dashboards-updater.zip 
unzip -v  ./dist/cloudwatch-dashboards-updater.zip  || true

cd ./terraform
terraform init
terraform validate
terraform plan -out=plan.tfplan
terraform apply -auto-approve plan.tfplan
