def calculate_energy(wcet, power):
    return power * wcet / 1000  # Convert mW to J

def find_min_energy_wcet(wcets, power_levels):
    min_energy = float('inf')
    min_energy_wcet = None
    min_energy_freq = None

    for i, wcet in enumerate(wcets):
        energy = calculate_energy(wcet, power_levels[i])
        if energy < min_energy:
            min_energy = energy
            min_energy_wcet = wcet
            min_energy_freq = [1188, 918, 648, 384][i]

    return min_energy_wcet, min_energy_freq, min_energy

def schedule_edfee(tasks, exec_time, power_levels):
    time = 0
    output = []

    while time < exec_time:
        if not tasks:
            break

        tasks.sort(key=lambda x: x[1])  # Sort by deadline
        current_task = tasks.pop(0)
        task_name, deadline, wcets = current_task

        wcet, frequency, energy = find_min_energy_wcet(wcets, power_levels)

        # Check if the task can be completed before its deadline
        if time + wcet <= deadline:
            output.append(f"{time} {task_name} {frequency} {wcet} {energy:.3f}J")
            time += wcet
        else:
            # Handle task missing its deadline
            print(f"Task {task_name} missed its deadline.")

        # Handle idle time
        if tasks:
            next_deadline = tasks[0][1]
            idle_time = next_deadline - time
            if idle_time > 0:
                idle_power = power_levels[-1]  # Idle at lowest frequency
                idle_energy = calculate_energy(idle_time, idle_power)
                output.append(f"{time} IDLE IDLE {idle_time} {idle_energy:.3f}J")
                time += idle_time

    return output
