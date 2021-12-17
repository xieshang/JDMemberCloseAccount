#!/bin/bash

sed -i 's/headless: false/headless: true/g' ./config.yaml
sed -i 's/binary: ""/binary: "/bin/chromium-browser"/g' ./config.yaml