#!/bin/bash

count=5
commands=(
    "./baseline"
    "./multitasking"
)
pattern="Total CPU time taken in seconds:"

output_files=(
    "baseline_times.txt"
    "multitasking_times.txt"
)

# create files
for file in "${output_files[@]}"; do
  >> "$file"
done


for ((i = 0; i < ${#commands[@]};i++)); do
    command="${commands[i]}"
    output_file="${output_files[$i]}"
    total_time=0
    for((j=1; j<= $count; j++)); do
        echo "Running $command - Attempt $j"
        output="$($command)"
        echo "$output" >> "$output_file"
        
        # Extract the CPU time from the output and accumulate it for averaging
        cpu_time=$(echo "$output" | grep "$pattern" | awk '{print $NF}')
        total_time=$(awk "BEGIN {print $total_time + $cpu_time}")
        wait
    done

    average_time=$(awk "BEGIN {print $total_time / $count}")
    echo "Average CPU time for $command: $average_time seconds"
done

echo "Finished running all commands the specified number of times."

