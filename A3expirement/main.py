import sys

def parse_input(file_name):
    tasks = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        system_params = list(map(int, lines[0].split()))
        num_tasks, exec_time, power_levels = system_params[0], system_params[1], system_params[2:]

        for line in lines[1:]:
            task_info = line.split()
            task_name = task_info[0]
            deadline = int(task_info[1])
            wcets = list(map(int, task_info[2:]))
            tasks.append((task_name, deadline, wcets))
    
    return num_tasks, exec_time, power_levels, tasks

def calculate_energy(frequency, time, power_levels):
    power_index = {1188: 2, 918: 3, 648: 4, 384: 5}
    # Validate if the frequency is in the power_index
    if frequency in power_index:
        index = power_index[frequency]
        # Check if index is within the range of power_levels
        if index < len(power_levels):
            power = power_levels[index]
            return power * time / 1000  # Convert mW to J
    return 0  # Return 0 if the frequency is not found or index is out of range

def schedule_edf(tasks, exec_time, power_levels):
    time = 0
    output = []

    while time < exec_time:
        if not tasks:
            break  # Exit loop if no tasks are remaining

        tasks.sort(key=lambda x: x[1])  # Sort by deadline
        current_task = tasks.pop(0)
        task_name, deadline, wcets = current_task

        # Choose the highest frequency for simplicity
        frequency = 1188
        wcet = wcets[0]
        energy = calculate_energy(frequency, wcet, power_levels)

        output.append(f"{time} {task_name} {frequency} {wcet} {energy:.3f}J")
        time += wcet

        # Handle idle time
        if tasks:
            next_deadline = tasks[0][1]
            idle_time = next_deadline - time
            if idle_time > 0:
                idle_energy = calculate_energy(384, idle_time, power_levels)  # Idle at lowest frequency
                output.append(f"{time} IDLE IDLE {idle_time} {idle_energy:.3f}J")
                time += idle_time

    return output


def write_output(output, file_name='output.txt'):
    with open(file_name, 'w') as file:
        for line in output:
            file.write(line + '\n')

def main():
    if len(sys.argv) < 3:
        print("Usage: your_program <input_file_name> <EDF or RM> [EE]")
        return

    file_name = sys.argv[1]
    num_tasks, exec_time, power_levels, tasks = parse_input(file_name)

    if sys.argv[2] == 'EDF':
        output = schedule_edf(tasks, exec_time, power_levels)
        write_output(output)
    else:
        print("Only EDF scheduling is implemented.")

if __name__ == "__main__":
    main()
