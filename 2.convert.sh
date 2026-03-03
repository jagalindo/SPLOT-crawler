#!/bin/bash
set -euo pipefail

# Directory to traverse
dir="./splot-xml"
output_fama="./fama-xml"
output_uvl="./flama-uvl"

# Ensure output directories exist
mkdir -p "$output_fama" "$output_uvl"

# Remove previous generated models to avoid possible append problems
find "$output_fama" -type f -delete 2>/dev/null || true
find "$output_uvl" -type f -delete 2>/dev/null || true

success=0
failed=0

# Iterate over each XML file in the source directory
for file in "$dir"/*.xml; do
  [ -f "$file" ] || continue

  filename=$(basename -- "$file" .xml)

  destination_fama="${output_fama}/${filename}.xml"
  if java -jar ./file_conversions/splx_to_fama.jar "$file" "$destination_fama" 2>/dev/null; then
    destination_uvl="${output_uvl}/${filename}.uvl"
    if python ./file_conversions/fama_to_uvl.py "$destination_fama" "$destination_uvl" 2>/dev/null; then
      success=$((success + 1))
    else
      echo "WARNING: UVL conversion failed for $filename" >&2
      failed=$((failed + 1))
    fi
  else
    echo "WARNING: FAMA conversion failed for $filename" >&2
    failed=$((failed + 1))
  fi
done

echo "Conversion complete. Success: $success, Failed: $failed"
