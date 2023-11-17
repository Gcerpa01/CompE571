import sys
from EDF import schedule_edf
from EDFEE import schedule_edfee

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

def write_output(output, file_name='output.txt'):
    with open(file_name, 'w') as file:
        for line in output:
            print(line)

def main():
    if len(sys.argv) < 3:
        print("Usage: your_program <input_file_name> <EDF or RM> [EE]")
        return

    file_name = sys.argv[1]
    scheduling_policy = sys.argv[2]
    energy_efficient = len(sys.argv) > 3 and sys.argv[3] == 'EE'

    num_tasks, exec_time, power_levels, tasks = parse_input(file_name)

    if scheduling_policy == 'EDF':
        if energy_efficient:
            # Call energy-efficient EDF scheduler
            output = schedule_edfee(tasks, exec_time, power_levels)
        else:
            # Call standard EDF scheduler
            # Assuming you have a separate function for standard EDF
            output = schedule_edf(tasks, exec_time, power_levels)
        write_output(output)
    else:
        print("Only EDF scheduling is implemented.")


if __name__ == "__main__":
    main()
