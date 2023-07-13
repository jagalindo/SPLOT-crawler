#!/bin/bash

# Output file
output_file="README.md"

# Remove the output file if it already exists
if [ -f "$output_file" ]; then
  rm "$output_file"
fi

# Hardcoded list of directories
directories=("./splot-xml" "./fama-xml" "./flama-uvl")

echo "This is the list of SPLOT models as of " $(date) >> "$output_file"
# Loop over each directory in the list
for dir in "${directories[@]}"
do
  # Check if the directory exists
  if [ -d "$dir" ]; then
    # Count the number of files in the directory
    num_files=$(find "$dir" -type f | wc -l)

    # Get the total size of the files in the directory in bytes
    total_size=$(du -sb "$dir" | cut -f1)

    # Append the summary for the current directory to the output file
    echo "## Directory: $dir" >> "$output_file"
    echo "Number of files: $num_files" >> "$output_file"
    echo "Total size: $total_size bytes" >> "$output_file"

    # List each file with its size
    #echo "### File List:" >> "$output_file"
    #find "$dir" -type f -exec du -sh {} \; >> "$output_file"

    #echo "---------------------------------" >> "$output_file"
  else
    echo "The directory $dir does not exist."
  fi
done