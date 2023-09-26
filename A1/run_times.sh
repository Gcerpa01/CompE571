count=50
commands=(
    "./baseline"
    "./multithreading"
    "./multitasking"
    "./popen"
)

pattern="Total CPU time taken in seconds:"

output_files=(
    "baseline_times.txt"
    "multithreading_times.txt"
    "multitasking_times.txt"
    "popen_times.txt"
)

# Function to print a text-based progress bar
# This was added for visualization - Sourced from CHATGPT AI #
print_progress() {
    local progress=$(( $1 * 50 / $count ))
    local bar=$(printf "%0.s=" $(seq 1 $progress))
    local space=$(printf "%0.s " $(seq $((50 - $progress))))
    printf "[$bar$space] %d%%\r" "$((progress * 2))"
}


# create files
for file in "${output_files[@]}"; do
  > "$file"
done

for ((i = 0; i < ${#commands[@]}; i++)); do
    command="${commands[i]}"
    echo "Starting $count iteration of $command"
    output_file="${output_files[$i]}"
    total_time=0
    times=()
    for ((j = 1; j <= $count; j++)); do
        # echo "Running $command - Attempt $j"
        output="$($command)" # save output of execute
        echo "$output" >> "$output_file" # save it to a text file

        # Extract the CPU time from the output and accumulate it for averaging
        cpu_time=$(echo "$output" | grep "$pattern" | awk '{print $NF}')
        total_time=$(awk "BEGIN {print $total_time + $cpu_time}")
        times+=("$cpu_time") # append to times
        wait

        print_progress $j
    done

    average_time=$(awk "BEGIN {print $total_time / $count}")
    echo "Average CPU time for $command: $average_time seconds"

    sum=0
    for time in "${times[@]}"; do
        diff=$(awk "BEGIN {print $time - $average_time}")
        diff_square=$(awk "BEGIN {print $diff * $diff}")
        sum=$(awk "BEGIN {print $sum + $diff_square}")
    done

    variance=$(awk "BEGIN {print $sum / $count}")
    std_dev=$(awk "BEGIN {print sqrt($variance)}")
    echo "Standard Deviation for $command: $std_dev seconds"
    echo
done

echo "Finished running all commands for $count times each"
