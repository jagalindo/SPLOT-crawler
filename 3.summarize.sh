#!/bin/bash
set -euo pipefail

output_file="README.md"

# Recreate the output file with a header
cat > "$output_file" <<EOF
# SPLOT Feature Models Repository

This is the list of SPLOT models as of $(date). You can parse the statistics using the \`statistics.json\` file.

EOF

# Hardcoded list of directories
directories=("./splot-xml" "./fama-xml" "./flama-uvl")

for dir in "${directories[@]}"; do
  if [ -d "$dir" ]; then
    num_files=$(find "$dir" -type f | wc -l)
    total_size=$(du -sh "$dir" | cut -f1)

    cat >> "$output_file" <<EOF
## Directory: $dir
- **Number of files:** $num_files
- **Total size:** $total_size

EOF
  else
    echo "WARNING: Directory $dir does not exist" >&2
  fi
done

echo "README generated at $output_file"
