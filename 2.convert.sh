#!/bin/bash

# Directory to traverse
dir="./splot-xml"
output_fama="./fama-xml"
output_uvl="./flama-uvl"

# Iterate over each XML file in the source directory
for file in "$dir"/*.xml
do
  filename=$(basename -- "$file" .xml)  
  
  destination_fama="${output_fama}/${filename}.xml"
  java -jar ./file_conversions/splx_to_fama.jar "$file" "$destination_fama"

  destination_uvl="${output_uvl}/${filename}.uvl"
  python ./file_conversions/fama_to_uvl.py "$destination_fama" "$destination_uvl"
done