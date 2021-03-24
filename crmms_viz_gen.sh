#!/bin/bash

echo "Activating Virtual Environment..."
readonly sourceFile="{$1}/bin/activate"

source ${sourceFile}

echo "Virtual Environment Activated!"

readonly projDir=$(pwd)

cd ${projDir}

readonly pyFile="./crmms_viz_gen.py"

echo "Starting CRMMS plots generation..."

python ${pyFile} --config $2 --output $3 --config_path $4 --provisional

echo "Process Complete!"

rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi