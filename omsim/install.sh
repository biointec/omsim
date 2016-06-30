#!/bin/bash
./package.sh
cd dist
pip uninstall -y omsim
pip install --user omsim-0.3.0-py2-none-any.whl
#pip3 uninstall -y omsim
#pip3 install --user omsim-0.3.0-py3-none-any.whl
cd ..
