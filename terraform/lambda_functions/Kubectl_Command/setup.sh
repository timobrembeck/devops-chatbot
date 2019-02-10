#!/usr/bin/env bash

pip3 install kubernetes --target .
cp ~/.kube/config .
chmod a+r config

echo "kubectl config has been copied."